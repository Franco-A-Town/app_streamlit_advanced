import streamlit as st
import pandas as pd
import time
from elements import bq_to_df, df_to_bq, df_to_bq_safe, active_dfa, commit, get_is_editing, update_is_editing    

#if 'dfa' not in st.session_state:
#    st.session_state.dfa = bq_to_df()
#
#st.session_state.dfa = bq_to_df()

def edit():

    if st.experimental_user.email in st.session_state.editor_user:

        st.subheader("Filter and edit data")

        # Crear campos de entrada para filtrar por Banner, Week y Year
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            banner_name = st.text_input("Search for Banner name")
        with col_2:    
            week = st.slider("Search for Week range", min_value=1, max_value=52, value=(1, 52))
        with col_3:    
            year = st.number_input("Search for Year", min_value=2023, max_value=2025, step=1, value=2025)

        # Aplicar filtros al DataFrame
        st.session_state["dfa"]["Active"] = False  # Desactivar todas las filas inicialmente

        # Filtrar por Banner, Week y Year
        st.session_state["dfa"].loc[
            (st.session_state["dfa"]["Banner"].str.contains(banner_name, case=False, na=False)) &
            (st.session_state["dfa"]["Week"] >= week[0]) &
            (st.session_state["dfa"]["Week"] <= week[1]) &
            (st.session_state["dfa"]["Year"] == year),
            "Active"
        ] = True

        # Mostrar el editor de datos para las filas activas
        edited_dfa = st.data_editor(
            active_dfa(),  # Mostrar solo las filas activas
            key="editor",
            on_change=commit  # Llamar a la función commit al realizar cambios
        )

        #st.write(active_dfa())

        col1, col2,col3 = st.columns([1,1,4])

        with col1:
            confirm_edit= st.button ("⬆️ Upload")

        with col2:
            if st.button ("❌ Cancel"):
                update_is_editing(new_value=False , user_email=st.experimental_user.email)
                st.session_state.is_editing = False
                st.session_state.is_editing = get_is_editing()
                if 'dfa' in st.session_state:
                    del st.session_state["dfa"]
                #st.write("{st.session_state.is_editing}")
                st.rerun()

        if confirm_edit:
            df_to_bq_safe(st.session_state["dfa"])
            update_is_editing(new_value=False , user_email=st.experimental_user.email)
            st.session_state.is_editing = get_is_editing()
            st.session_state.df = bq_to_df()
            if 'dfa' in st.session_state:
                del st.session_state["dfa"]
            st.rerun()
    
    else:
        st.warning("Editor role is needed. Please contact the administrator.")
        
import streamlit as st
import pandas as pd
from elements import banners, create_register, bq_to_df, filter_df, get_is_editing, default_form_values
import time

if "df" not in st.session_state:
    st.session_state.df = bq_to_df()

def input():

    if 'is_df_filtered' not in st.session_state:
        st.session_state.is_df_filtered = False

    # Usamos session_state para controlar el flujo
    if 'show_confirmation' not in st.session_state:
        st.session_state.show_confirmation = False
    if 'form_data' not in st.session_state:
        st.session_state.form_data = default_form_values
    if 'clear_on_submit' not in st.session_state:
        st.session_state.clear_on_submit = False

    # Formulario principal
    if st.session_state.show_confirmation== False and st.session_state.is_editing== False:
        st.subheader("Create and upload new performance data registers")
        with st.form("create", clear_on_submit=st.session_state.clear_on_submit):
            col_1, col_2, col_3, col_4, col_5, col_6 = st.columns([2,2,2,2,2,3])

            with col_1:
                year = st.session_state.form_data['year']
                banner_input = [banner for banner in banners if banner != "All banners"]
                banner = st.selectbox("Select banner", 
                                      banner_input, 
                                      index=banner_input.index(st.session_state.form_data['banner']))
                week = st.number_input("Number of week", min_value=1, max_value=52,
                                       value=st.session_state.form_data['week'])

            
            with col_2:
                traffic = st.number_input("Traffic", min_value=0, 
                                          value=st.session_state.form_data['traffic'])
                transactions = st.number_input("Transactions", min_value=0,
                                               value=st.session_state.form_data['transactions'])
                appointments = st.number_input("Appointments", min_value=0, 
                                               value=st.session_state.form_data['appointments'])
                total_revenue = st.number_input("Total revenues", min_value=0.0,
                                                value=st.session_state.form_data['revenue'])
                total_return_values = st.number_input("Total return value", min_value=0.0,
                                                      value=st.session_state.form_data['total_return_values'])

            with col_3:
                cl_revenues = st.number_input("Contact lenses revenues", min_value=0.0,
                                              value=st.session_state.form_data['cl_revenue'])
                cl_return_values = st.number_input("Contact lenses return values", min_value=0.0,
                                                   value=st.session_state.form_data['cl_return_values'])
                cl_units = st.number_input("Contact lenses units", min_value=0,
                                           value=st.session_state.form_data['cl_units'])

            with col_4:
                opt_revenues = st.number_input("Optical revenues", min_value=0.0,
                                               value=st.session_state.form_data['opt_revenue'])
                opt_return_values = st.number_input("Optical return values", min_value=0.0,
                                                    value=st.session_state.form_data['opt_return_values'])
                opt_units = st.number_input("Optical units", min_value=0,
                                            value=st.session_state.form_data['opt_units'])

            with col_5:
                sun_revenues = st.number_input("Sun glasses revenues", min_value=0.0,
                                               value=st.session_state.form_data['sun_revenue'])
                sun_return_values = st.number_input("Sun glasses return values", min_value=0.0,
                                                    value=st.session_state.form_data['sun_return_values'])
                sun_units = st.number_input("Sun glasses units", min_value=0,
                                            value=st.session_state.form_data['sun_units'])

            with col_6:
                insights_on_performance = st.text_area("Insights on performance",
                                                       value=st.session_state.form_data['insights_on_performance'])
                insights_on_blockers = st.text_area("Insights on blockers",
                                                    value=st.session_state.form_data['insights_on_blockers'])

            submitted = st.form_submit_button("Upload to BQ")

            if submitted:
                st.session_state.is_editing = get_is_editing()
                if st.session_state.is_editing== False:
                # Guardar los datos en session_state
                    #if "form_data" not in st.session_state: 
                    st.session_state.form_data = {
                        'year': year,
                        'week': week,
                        'banner': banner,
                        'traffic': traffic,
                        'transactions': transactions,
                        'revenue': total_revenue,
                        'insights_on_performance': insights_on_performance,
                        'insights_on_blockers': insights_on_blockers,
                        'sun_revenue': sun_revenues,
                        'sun_units': sun_units,
                        'cl_revenue': cl_revenues,
                        'cl_units': cl_units,
                        'opt_revenue': opt_revenues,
                        'opt_units': opt_units,
                        'total_return_values': total_return_values,
                        'cl_return_values': cl_return_values,
                        'opt_return_values': opt_return_values,
                        'sun_return_values': sun_return_values,
                        'appointments': appointments
                    }
                    st.session_state.show_confirmation = True
                    st.rerun()
                else:
                    st.warning("The data can not be upload because they are being edited")
                    st.session_state.show_confirmation = False
                    st.session_state.form_data = None
                    time.sleep(3)
                    st.rerun()

    # Pantalla de confirmación
    if st.session_state.show_confirmation and st.session_state.form_data:
        confirm_container = st.container()
        with confirm_container:
            st.subheader("Please check the data entered before upload")
            # Mostrar los datos ingresados
            col_1, col_2, col_3 = st.columns([1,1,2])
            with col_1:
                st.json({
                    'Year': st.session_state.form_data['year'],
                    'Week': st.session_state.form_data['week'],
                    'Banner': st.session_state.form_data['banner'],
                    'Traffic': st.session_state.form_data['traffic'],
                    'Transactions': st.session_state.form_data['transactions'],
                    'Appointments': st.session_state.form_data['appointments'],
                    'Total revenues': st.session_state.form_data['revenue'],
                    'Total return values': st.session_state.form_data['total_return_values']
                })
    
            with col_2:
                st.json({
                    'Sun revenues': st.session_state.form_data['sun_revenue'],
                    'Sun return values': st.session_state.form_data['sun_return_values'],
                    'Sun units': st.session_state.form_data['sun_units'],
                    'CL revenues': st.session_state.form_data['cl_revenue'],
                    'CL return values': st.session_state.form_data['cl_return_values'],            
                    'CL units': st.session_state.form_data['cl_units'],
                    'OPT revenues': st.session_state.form_data['opt_revenue'],
                    'OPT return values': st.session_state.form_data['opt_return_values'],            
                    'OPT units': st.session_state.form_data['opt_units']
                })
    
            with col_3:
                st.json({
                    'Insights on performance': st.session_state.form_data['insights_on_performance'],
                    'Insights on blockers': st.session_state.form_data['insights_on_blockers']
                })
            
            col1, col2, col3 = st.columns([1,1,4])
            with col1:
                confirm_input = st.button("✅ Upload")
            
            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.show_confirmation = False
                    st.session_state.clear_on_submit = False
                    st.rerun()
        
            if confirm_input:
                st.session_state.is_editing = get_is_editing()
                if st.session_state.is_editing== False:
                    banner = st.session_state.form_data['banner']
                    year = st.session_state.form_data['year']
                    week = st.session_state.form_data['week']

                    if f"{banner.replace(' ','')}-{year}-{week}" in set(st.session_state.df['id']):
                        st.error("The register for the Banner, Year and Week entered already exists")
                        time.sleep(3)
                        st.session_state.show_confirmation = False
                        st.session_state.clear_on_submit = False
                        st.rerun()
                    else:
                        # Subir los datos
                        create_register(**st.session_state.form_data)
                        st.session_state.df= bq_to_df()
                        st.session_state.show_confirmation = False
                        st.session_state.form_data = default_form_values
                        st.rerun()
                else:
                    st.warning("The data can not be upload because they are being edited")
                    time.sleep(3)
                    st.session_state.show_confirmation = False
                    st.session_state.form_data = None
                    st.rerun()

    # Formulario de filtrado
    with st.form("filter_input", clear_on_submit=True):
        st.subheader("Visualize updated performance data registers")
        col_1, col_2, col_3 = st.columns(3)

        with col_1:
            year = st.multiselect("Select year", [2023, 2024, 2025])
        with col_2:
            week = st.slider("Range of weeks", min_value=1, max_value=52, value=(1, 52))
        with col_3:
            banner = st.multiselect("Select banner", banners)
            if 'All banners' in banner:
                banner = banners

        filter = st.form_submit_button(label="Filter")
        if filter:
            df_filtered = filter_df(df= st.session_state.df, filter_year=year, filter_week=week, filter_banner=banner)
            st.session_state.is_df_filtered = True
    
    if st.session_state.is_df_filtered:
        st.write(df_filtered)
    else:
        st.write(st.session_state.df)



if __name__ == "__input__":
    input()
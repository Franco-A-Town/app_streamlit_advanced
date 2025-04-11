import streamlit as st
from PIL import Image
from elements import bq_to_df, get_is_editing, update_is_editing
from input import input
from edit import edit
import time

if "is_editing" not in st.session_state:
    st.session_state.is_editing = get_is_editing()

if "df" not in st.session_state:
    st.session_state.df = bq_to_df()

icon = Image.open("icon.jpeg")

st.set_page_config(
    page_title="Source Data App",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Source Data App")

if not st.experimental_user.is_logged_in:
    st.subheader("Please log-in to continue")
    if st.button("Log In"):
        st.login("google")

else:
    st.subheader(f"Welcome {st.experimental_user.email}")

    if st.button("Logout"):
       st.logout()
       st.session_state.is_logged_in = False

    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Select an option", ("Input", "Edit"))
    if menu == "Input":
        st.session_state.is_editing = get_is_editing()
        if st.session_state.is_editing==False:
            input()
        else:
            st.warning("**Upload** of new registers **Disabled**. The data are being edited. " \
            "Please refresh the app before uploading new data")
            input()
            #time.sleep(3)
            #st.rerun()
    elif menu == "Edit":
        st.session_state.is_editing = get_is_editing()
        if st.session_state.is_editing==False:
            st.warning("Press the button below to edit the data. " \
            "The upload of **new registers** will be **disabled** during the edition process")

            if st.button("Edit Data"):
                update_is_editing(True)
                st.session_state.is_editing = get_is_editing()
                st.rerun()
        else:
            edit()

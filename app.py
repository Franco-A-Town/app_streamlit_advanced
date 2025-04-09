import streamlit as st
from PIL import Image
from elements import bq_to_df, get_is_editing, update_is_editing
from input import input
from edit import edit

# Configuración de página primero
icon = Image.open("icon.jpeg")
st.set_page_config(
    page_title="Source Data App",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="auto",  # Cambiado de "collapsed"
)

# CSS personalizado para asegurar la barra lateral
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 300px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Inicialización de estado
if "is_editing" not in st.session_state:
    st.session_state.is_editing = get_is_editing()

if "df" not in st.session_state:
    st.session_state.df = bq_to_df()

st.title("Source Data App")

if not st.experimental_user.is_logged_in:
    st.header("Please log-in to continue")
    if st.button("Log In"):
        st.login("google")
else:
    if st.button("Logout"):
       st.logout()
       st.session_state.is_logged_in = False

    # Barra lateral solo cuando está logueado
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Select an option", ("Input", "Edit"))
    
    if menu == "Input":
        if st.session_state.is_editing==False:
            input()
        else:
            st.warning("The data are being edited. Please wait until " \
            "the edition is finished before uploading new data")
    elif menu == "Edit":
        if st.session_state.is_editing==False:
            st.info("Press the button below to edit the data. The input of new registers will be disabled")
            if st.button("Edit Data"):
                update_is_editing(True)
                st.session_state.is_editing = get_is_editing()
                st.rerun()
        else:
            edit()
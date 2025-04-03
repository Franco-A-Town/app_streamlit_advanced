import streamlit as st
from PIL import Image
from input import input

icon = Image.open("icon.jpeg")

st.set_page_config(
    page_title="Source Data App",
    page_icon=icon,
    layout="wide",
)

# Botón de login
if st.button("Login"):
    st.login("google")
    st.json(st.experimental_user)

# Verificar condiciones para renderizar input()
if st.experimental_user.is_logged_in:
    input()
import streamlit as st

st.title("Authentication")

if st.button("Login"):
    st.login("google")

if st.button("Logout"):
    st.logout()

st.json(st.experimental_user)
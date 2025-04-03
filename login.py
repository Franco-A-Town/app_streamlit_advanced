import streamlit as st

def login():
    st.title("Authentication")

    if st.button ("Login"):
        st.login("google")

if __name__ == "__login__":
    login()
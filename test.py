from elements import banners, default_form_values
import streamlit as st

if 'form_data' not in st.session_state:
    st.session_state.form_data = default_form_values

banner_input = [banner for banner in banners if banner != "All banners"]

banner_input.index(st.session_state.form_data['banner'])
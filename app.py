import streamlit as st
from PIL import Image
from elements import bq_to_df, get_is_editing, update_is_editing, get_user_is_editing
from input import input
from edit import edit
import time

if "is_editing" not in st.session_state:
    st.session_state.is_editing = get_is_editing()

if "df" not in st.session_state:
    st.session_state.df = bq_to_df()

editor= st.secrets.user_role.editor
editor_user_set = set(email.strip().strip('"') for email in editor.split(','))

entry= st.secrets.user_role.entry
entry_user_set = set(email.strip().strip('"') for email in entry.split(','))

if "editor_user" not in st.session_state:
    st.session_state.editor_user = editor_user_set

icon = Image.open("icon.jpeg")

st.set_page_config(
    page_title="Source Data App",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Source Data App", anchor= False)

if not st.experimental_user.is_logged_in:
    st.subheader("Please login to continue", anchor= False)
    if st.button("🔑 Login"):
        st.login("google")

else:
    if st.experimental_user.email and st.experimental_user.email.lower() in (
        email.lower() for email in entry_user_set | editor_user_set
        ):
        
        st.subheader(f"Welcome {st.experimental_user.email}" , anchor= False)
        
        if st.experimental_user.email in st.session_state.editor_user:
            st.info("Role: Editor")
        else:
            st.info("Role: Data entry")
        
        col_1, col_2 = st.columns([6,1])
        
        with col_2:
            if st.button("👋 Logout", use_container_width=True):
               st.session_state.is_logged_in = False
               st.logout()

        st.sidebar.title("Menu")
        menu = st.sidebar.radio("Select an option", ("Input", "Edit"))

        if menu == "Input":
            st.session_state.is_editing = get_is_editing()
            if st.session_state.is_editing==False:
                input()
            else:
                st.warning(f"**Upload** of new registers **Disabled**. The data are being edited by {get_user_is_editing()}. " \
                "Please refresh the app and try uploading again later. ")
                input()
                #time.sleep(3)
                #st.rerun()

        elif menu == "Edit":
            if st.experimental_user.email in st.session_state.editor_user:
                st.session_state.is_editing = get_is_editing()
                if st.session_state.is_editing==False:
                    st.warning("Click below to edit. Other users won't be able to add records or modify data until you're done.")

                    if st.button("✏️ Edit Data"):
                        update_is_editing(True, user_email=st.experimental_user.email)
                        #st.session_state.df = bq_to_df()
                        st.session_state.is_editing = get_is_editing()
                        st.rerun()
                else:
                    if get_user_is_editing() == st.experimental_user.email:
                        if 'dfa' not in st.session_state:
                            st.session_state.dfa = bq_to_df()
                        
                        edit()
                    else:
                        st.error(f"Editing has already been activated by user {get_user_is_editing()}. ")
            else:
                st.error("**Editor role** is needed. Please contact the administrator.")

    else:
        st.error(f"Hi {st.experimental_user.email}. Your user email does not have permission to access this app. " \
        "Please contact the administrator.")
        st.session_state.is_logged_in = False
        time.sleep(7)
        st.logout()
import streamlit as st
import pandas as pd
import time

# Inicializa un DataFrame en el estado de sesión si no existe
if "dfa" not in st.session_state:
    st.session_state["dfa"] = pd.DataFrame(
        {
            "Par": ["Apple", "Strawberry", "Banana"],  # Columna con nombres de frutas
            "Cat1": ["good", "good", "bad"],  # Columna con categorías (ejemplo: calidad)
            "Cat2": ["healthy", "healthy", "unhealthy"],  # Columna con categorías (ejemplo: salud)
            "Active": [False, False, False],  # Columna para marcar si una fila está activa
        }
    )

# Función para filtrar las filas activas del DataFrame
def active_dfa():
    # Devuelve una copia del DataFrame donde la columna "Active" es True
    return st.session_state["dfa"][st.session_state["dfa"]["Active"] == True].copy()

# Función para obtener el índice de una fila activa
def get_index(row):
    # Devuelve el índice de la fila activa en el DataFrame original
    return active_dfa().iloc[row].name

# Función para guardar los cambios realizados en el editor
def commit():
    # Itera sobre las filas editadas en el editor
    for row in st.session_state.editor["edited_rows"]:
        row_index = get_index(row)  # Obtiene el índice de la fila activa
        # Actualiza los valores editados en el DataFrame original
        for key, value in st.session_state.editor["edited_rows"][row].items():
            st.session_state["dfa"].at[row_index, key] = value

# Título de la aplicación
st.header("Filter and edit data")

# Campo de texto para buscar en la columna "Par"
name = st.text_input("Search for ...")

# Si no se ingresa texto, activa todas las filas
if name == "":
    st.session_state["dfa"].Active = True
else:
    # Si se ingresa texto, desactiva todas las filas
    st.session_state["dfa"].Active = False
    # Activa solo las filas donde la columna "Par" contiene el texto ingresado
    st.session_state["dfa"].loc[
        st.session_state["dfa"]["Par"].str.contains(name, case=False), "Active"
    ] = True

# Editor de datos interactivo para las filas activas
edited_dfa = st.data_editor(
    active_dfa(),  # Muestra solo las filas activas
    column_order=["Par", "Cat1", "Cat2"],  # Orden de las columnas en el editor
    key="editor",  # Clave para identificar el editor en el estado de sesión
    on_change=commit,  # Llama a la función commit() cuando se realizan cambios
)
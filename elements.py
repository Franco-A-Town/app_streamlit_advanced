import streamlit
import pandas as pd
import re


banners= [
    'All banners',
    'AT - Pearle',
    'BE - Pearle',
    'BG - Vision Express',
    'CH - Kochoptik',
    'CH - Linsenmax',
    'CH - McOptic',
    'CH - Visilab',
    'CZ - GrandOptical',
    'DE - Apollo',
    'DE - RobinLook',
    'DK - Synoptik',
    'EE - Instrumentarium Optika',
    'ES - MasVision',
    'ES - Optica2000',
    'FI - Instrumentarium',
    'FI - Keops',
    'FI - Nissen',
    "FR - Generale d'Optique",
    'FR - GrandOptical',
    'HU - Ofotert',
    'HU - Vision Express',
    'NL - GrandOptical',
    'NL - Pearle',
    'NO - Brilleland',
    'NO - Interoptik',
    'PL - Vision Express',
    'PT - MultiOpticas',
    'RU - LensMaster',
    'SE - Synoptik',
    'SK - GrandOptical',
    'TR - Atasun',
    'UKI - Vision Express',
    'IT - GrandVision',
    'IT - Salmoiraghi & Viganò',
    'UK - David Clulow'
    ]



dict_header = {
    "year" : "Year" ,
    "week" : "Week" ,
    "banner" : "Banner" ,
    "traffic" : "Traffic" ,
    "transactions" : "Transactions" ,
    "revenue" : "Total revenue" ,
    "insights_on_performance" : "Insights on performance" ,
    "insights_on_blockers" : "Insights on blockers" ,
    "sun_revenue" : "Sun revenues" ,
    "sun_units" : "Sun units" ,
    "cl_revenue" : "CL revenues" ,
    "cl_units" : "CL units" ,
    "opt_revenue" : "OPT revenues" ,
    "opt_units" : "OPt units" ,
    "total_return_values" : "Return values" ,
    "cl_return_values" : "CL return_values" ,
    "opt_return_values" : "OPT return values" ,
    "sun_return_values" : "SUN return values" ,
    "appointments" : "Appointments"
}



from google.cloud import bigquery
from google.oauth2 import service_account  # Importamos service_account para usar credenciales directamente
import streamlit as st

## Crear credenciales directamente desde el diccionario
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(credentials=credentials)


project_id = "circular-cubist-455115-m2"
dataset_id = "app_source_data"
source_data_table_id = "app_source_data"
source_data_table_ref = f"{project_id}.{dataset_id}.{source_data_table_id}"
is_editing_table_id = "is_editing"
is_editing_table_ref = f"{project_id}.{dataset_id}.{is_editing_table_id}"


def create_register(
        year=None,
        week=None,
        banner=None,
        traffic=None,
        transactions=None,
        revenue=None,
        insights_on_performance=None,
        insights_on_blockers=None,
        sun_revenue=None,
        sun_units=None,
        cl_revenue=None,
        cl_units=None,
        opt_revenue=None,
        opt_units=None,
        total_return_values=None,
        cl_return_values=None,
        opt_return_values=None,
        sun_return_values=None,
        appointments=None
):
    
    id = f"{banner.replace(' ','')}-{year}-{week}"

    rows_to_insert = [
        {
            "year": year,
            "week": week,
            "banner": banner,
            "traffic": traffic,
            "transactions": transactions,
            "revenue": revenue,
            "insights_on_performance": insights_on_performance,
            "insights_on_blockers": insights_on_blockers,
            "sun_revenue": sun_revenue,
            "sun_units": sun_units,
            "cl_revenue": cl_revenue,
            "cl_units": cl_units,
            "opt_revenue": opt_revenue,
            "opt_units": opt_units,
            "total_return_values": total_return_values,
            "cl_return_values": cl_return_values,
            "opt_return_values": opt_return_values,
            "sun_return_values": sun_return_values,
            "appointments": appointments,
            "id": id
        }
    ]
    df = bq_to_df()

    previous_ids = df['id']

    previous_ids = set(previous_ids)

    if id not in previous_ids:
        errors = client.insert_rows_json(source_data_table_ref, rows_to_insert)
        if errors:
            st.error("Error trying to insert register:", errors)
        else:
            st.success("New register uploaded to Big Query succesfully")
    else:
        st.error("The register for the Banner, Year and Week entered already exists")


def bq_to_df():
    # Obtener la tabla de BigQuery
    table = client.get_table(source_data_table_ref)  # Obtener la referencia de la tabla
    rows = client.list_rows(table)  # Listar todas las filas de la tabla
    df = rows.to_dataframe()  # Convertir las filas a un DataFrame de pandas

    # Seleccionar y renombrar columnas según el diccionario dict_header
    df = df[
        [
            "id",
            "year",
            "week",
            "banner",
            "traffic",
            "transactions",
            "appointments",
            "revenue",
            "total_return_values",
            "cl_revenue",
            "cl_return_values",
            "cl_units",
            "opt_revenue",
            "opt_return_values",
            "opt_units",
            "sun_revenue",
            "sun_return_values",
            "sun_units",
            "insights_on_performance",
            "insights_on_blockers",
        ]
    ]

    df.rename(columns=dict_header, inplace=True)

    # Ordenar las filas de forma ascendente según banner, year y week
    df.sort_values(by=["Banner", "Year", "Week"], ascending=True, inplace=True)

    return df


def filter_df(df: pd.DataFrame, 
               filter_year: list, 
               filter_week: tuple,
               filter_banner: list) -> pd.DataFrame:
    
    set_filter_year = set(filter_year)
    mask_year = df['Year'].isin(set_filter_year)

    set_filter_week = set(range(filter_week[0], filter_week[1] + 1))
    mask_week = df['Week'].isin(set_filter_week)

    set_filter_banner = set(filter_banner)
    mask_banner = df['Banner'].isin(set_filter_banner)

    result = df.loc[mask_year & mask_week & mask_banner, :]

    return result


def df_to_bq(df: pd.DataFrame):

    df = df.loc[:, df.columns != "Active"]
    df = df.rename(
        columns={
            "id": "id",
            "Year": "year",
            "Week": "week",
            "Banner": "banner",
            "Traffic": "traffic",
            "Transactions": "transactions",
            "Total revenue": "revenue",
            "Insights on performance": "insights_on_performance",
            "Insights on blockers": "insights_on_blockers",
            "Sun revenues": "sun_revenue",
            "Sun units": "sun_units",
            "CL revenues": "cl_revenue",
            "CL units": "cl_units",
            "OPT revenues": "opt_revenue",
            "OPt units": "opt_units",
            "Return values": "total_return_values",
            "CL return_values": "cl_return_values",
            "OPT return values": "opt_return_values",
            "SUN return values": "sun_return_values",
            "Appointments": "appointments"
            }
    )


    # Referencia a la tabla
    source_data_table_ref = f"{project_id}.{dataset_id}.{source_data_table_id}"

    # Borrar la tabla existente
    try:
        client.delete_table(source_data_table_ref)  # Elimina la tabla
        st.success(f"Table {source_data_table_ref} succesfully deleted")
    except Exception as e:
        st.error(f"Error deleting table: {e}")
        return

    # Crear un esquema basado en las columnas del DataFrame
    schema = [
        bigquery.SchemaField(column, str(df[column].dtype).replace("object", "STRING").replace("int64", "INTEGER").replace("float64", "FLOAT"))
        for column in df.columns
    ]

    # Crear una nueva tabla con el esquema
    table = bigquery.Table(source_data_table_ref, schema=schema)
    try:
        client.create_table(table)  # Crea la tabla vacía
        st.success(f"Table {source_data_table_ref} succesfully created")
    except Exception as e:
        st.error(f"Error when creating table: {e}")
        return

    # Cargar los datos del DataFrame en la tabla
    try:
        job = client.load_table_from_dataframe(df, source_data_table_ref)  # Carga el DataFrame en la tabla
        job.result()  # Espera a que el trabajo termine
        st.success(f"Data succesfully uploaded to table {source_data_table_ref}.")
    except Exception as e:
        st.error(f"Error when uploading data to table: {e}")

def active_dfa():
    return st.session_state["dfa"][st.session_state["dfa"]["Active"] == True].copy()


def get_index(row):
    return active_dfa().iloc[row].name


def commit():
    for row in st.session_state.editor["edited_rows"]:
        row_index = get_index(row)
        for key, value in st.session_state.editor["edited_rows"][row].items():
            st.session_state["dfa"].at[row_index, key] = value


def get_is_editing():
    query = f"""
        SELECT is_editing
        FROM `{is_editing_table_ref}`
        LIMIT 1
    """

    try:
        # Ejecutar la consulta
        query_job = client.query(query)

        # Esperar el resultado
        results = query_job.result()

        # Obtener el valor de la primera fila
        for row in results:
            return row.is_editing  # Retorna el valor booleano de la columna 'is_editing'

    except Exception as e:
        return None

def update_is_editing(new_value: bool):
    # Consulta para actualizar el primer registro
    query = f"""
    UPDATE `{is_editing_table_ref}`
    SET is_editing = @new_value
    WHERE TRUE  -- Esto asegura que se actualice aunque no haya condiciones específicas
    """
    # Configuramos los parámetros de la consulta
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("new_value", "BOOL", new_value)]
    )
    
    try:
        # Ejecutar la consulta
        client.query(query, job_config=job_config).result()
        print(f"")
    except Exception as e:
        print(f"Error updating: {e}")

'''
# Create the table in BigQuery
# This code is only needed once to create the table

CREATE OR REPLACE TABLE `circular-cubist-455115-m2.app_source_data.app_source_data` (
  id STRING,
  year INT64,
  week INT64,
  banner STRING,
  traffic INT64,
  transactions INT64,
  revenue FLOAT64,
  insights_on_performance STRING,
  insights_on_blockers STRING,
  sun_revenue FLOAT64,
  sun_units INT64,
  cl_revenue FLOAT64,
  cl_units INT64,
  opt_revenue FLOAT64,
  opt_units INT64,
  total_return_values FLOAT64,
  cl_return_values FLOAT64,
  opt_return_values FLOAT64,
  sun_return_values FLOAT64,
  appointments INT64
);
'''
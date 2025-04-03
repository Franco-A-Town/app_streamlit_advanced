import streamlit
import pandas as pd
import re

banners= [
    'Banner_1',
    'Banner_2',
    'Banner_3',
    'Banner_4']


'''
banners= [
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
'''


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


import os
import toml
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
table_id = "app_source_data"
table_ref = f"{project_id}.{dataset_id}.{table_id}"


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
        errors = client.insert_rows_json(table_ref, rows_to_insert)
        if errors:
            st.error("Error trying to insert register:", errors)
        else:
            st.success("New register uploaded to Big Query succesfully")
    else:
        st.error("The register for the Banner, Year and Week entered already exists")


def bq_to_df():
    # Construye la consulta SQL
    query = f"""
        SELECT *
        FROM `{table_ref}`
        ORDER BY banner ASC, year ASC, week ASC
    """

    # Ejecuta la consulta y convierte los resultados a DataFrame
    df = client.query(query).to_dataframe()

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
        "insights_on_blockers"
        ]
    ]

    df.rename(columns=dict_header, inplace=True)
    
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


def is_integer_number(value: str) -> bool:
    result = bool(re.match(r"^-?\d+$", value))
    if result:
        st.write('Es entero')
    else:
        st.write('No es entero')
    return result


def is_rational_number(value: str) -> bool:
    reg_exp = r"^-?\d+\.\d+$|^-?\d+$"
    return bool(re.match(reg_exp, value))
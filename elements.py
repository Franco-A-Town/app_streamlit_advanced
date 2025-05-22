import pandas as pd
from datetime import datetime, timezone
import time
from google.cloud import bigquery
from google.oauth2 import service_account  # Importamos service_account para usar credenciales directamente
import streamlit as st

banners= [
    'All banners',
    'Banner - 1',
    'Banner - 2',
    'Banner - 3',
    'Banner - 4',
    'Banner - 5']


'''
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

default_form_values = {
                        'year': 2025,
                        'week': 1,
                        'banner': banners[1],
                        'traffic': 0,
                        'transactions': 0,
                        'revenue': 0.00,
                        'insights_on_performance': "",
                        'insights_on_blockers': "",
                        'sun_revenue': 0.00,
                        'sun_units': 0,
                        'cl_revenue': 0.00,
                        'cl_units': 0,
                        'opt_revenue': 0.00,
                        'opt_units': 0,
                        'total_return_values': 0.00,
                        'cl_return_values': 0.00,
                        'opt_return_values': 0.00,
                        'sun_return_values': 0.00,
                        'appointments': 0
                    }

column_config = {
    "id": st.column_config.Column(disabled=True),  # Columna no editable
    "Year": st.column_config.NumberColumn("Year", format="%d", min_value=2023, max_value=2025),
    "Week": st.column_config.NumberColumn("Week", format="%d", min_value=1, max_value=52),
    "Banner": st.column_config.SelectboxColumn("Banner", options=banners, default=banners[1]),
    "Traffic": st.column_config.NumberColumn("Traffic", format="%d"),
    "Transactions": st.column_config.NumberColumn("Transactions", format="%d"),
    "Appointments": st.column_config.NumberColumn("Appointments", format="%d"),
    "Total revenue": st.column_config.NumberColumn("Total Revenue", format="%.2f"),
    "Return values": st.column_config.NumberColumn("Return Values", format="%.2f"),
    "CL revenues": st.column_config.NumberColumn("CL Revenues", format="%.2f"),
    "CL return_values": st.column_config.NumberColumn("CL Return Values", format="%.2f"),
    "CL units": st.column_config.NumberColumn("CL Units", format="%d"),
    "OPT revenues": st.column_config.NumberColumn("OPT Revenues", format="%.2f"),
    "OPT return values": st.column_config.NumberColumn("OPT Return Values", format="%.2f"),
    "OPT units": st.column_config.NumberColumn("OPT Units", format="%d"),
    "Sun revenues": st.column_config.NumberColumn("SUN Revenues", format="%.2f"),
    "Sun return values": st.column_config.NumberColumn("SUN Return Values", format="%.2f"),
    "Sun units": st.column_config.NumberColumn("SUN Units", format="%d"),
    "Insights on performance": st.column_config.TextColumn("Performance Insights"),
    "Insights on blockers": st.column_config.TextColumn("Blockers Insights")
}





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
    
    #id = f"{banner.replace(' ','')}-{year}-{week}"

    id = f"{st.experimental_user.email}.utc.{datetime.now(timezone.utc).isoformat()}"
    
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

    previous_year_banner_week = set(df["Year"].astype(str) + 
                                    df["Banner"].astype(str) + 
                                    df["Week"].astype(str))

    current_year_banner_week = str ( str(year) + str(banner) + str(week) )

    if current_year_banner_week not in previous_year_banner_week:
        errors = client.insert_rows_json(source_data_table_ref, rows_to_insert)
        if errors:
            st.error("Error trying to insert register:", errors)
        else:
            st.success("New register uploaded to Big Query succesfully")
    else:
        st.error(f"The register for the Banner '**{banner}**' , Year '**{year}**' and Week '**{week}**' entered already exists")
        time.sleep(3)
        st.session_state.show_confirmation = False
        st.session_state.clear_on_submit = False
        st.rerun()


def bq_to_df():
    
    query = f"""
    SELECT * 
    FROM `{source_data_table_ref}`
    """
    df = client.query(query).to_dataframe()

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


def df_to_bq_safe(edited_df: pd.DataFrame, table_id: str = 'circular-cubist-455115-m2.app_source_data.app_source_data'):
    
    """
    Safely updates main table with proper column name standardization
    and creates consistent backups in the partitioned table.
    Handles schema mismatches automatically.
    """

    #st.write(edited_df)
    try:
        # 1- Extract table information
        project_id, dataset_id, table_name = table_id.split('.')
        
        # 2- Standardize column names (applies to both backup and new data)
        column_mapping = {
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
        
        # Create processed DataFrame
        processed_df = edited_df.rename(columns=column_mapping)

        #st.write(processed_df)
        
        # 3- Remove any columns not in the target tables
        # Get schema for both tables
        backup_table_ref = f"{project_id}.{dataset_id}.backups_master"
        backup_table = client.get_table(backup_table_ref)
        main_table = client.get_table(table_id)
        
        # Combine valid columns from both tables
        valid_columns = {field.name for field in backup_table.schema}.union(
                        {field.name for field in main_table.schema})
        
        # Filter columns to only those that exist in destination tables
        processed_df = processed_df[[col for col in processed_df.columns 
                                  if col in valid_columns]]
        
        # 4- Create backup with corrected data
        backup_timestamp = pd.Timestamp.now(tz='UTC')
        backup_df = processed_df.copy()
        backup_df['backup_timestamp'] = backup_timestamp
        
        st.info("🔄 Creating backup in partitioned table...")
        #st.write(backup_df)
        client.load_table_from_dataframe(
            backup_df,
            backup_table_ref,
            job_config=bigquery.LoadJobConfig(
                write_disposition="WRITE_APPEND",
                schema_update_options=bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
            )
        ).result()
        st.success(f"✅ Backup created ({backup_timestamp})")
        
        # 5- Clear existing data from main table
        st.info("🗑️ Clearing old data from main table...")
        client.query(f"TRUNCATE TABLE `{table_id}`").result()
        
        # 6- Upload processed data to main table
        st.info("⬆️ Uploading edited data to main table...")
        client.load_table_from_dataframe(
            processed_df,
            table_id,
            job_config=bigquery.LoadJobConfig(
                write_disposition="WRITE_APPEND",
                schema_update_options=bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
            )
        ).result()
        
        # 7- Verify record count matches
        new_count = client.query(f"SELECT COUNT(*) FROM `{table_id}`").result().to_dataframe().iloc[0,0]
        if new_count == len(processed_df):
            st.success("🎉 Database updated successfully!")
        else:
            raise Exception("❌ Record count mismatch")
            
    except Exception as e:
        st.error(f"🚨 Error: {str(e)}")
        st.warning("🔙 Attempting to restore from most recent backup...")
        
        try:
            # Get the most recent backup (already with standardized column names)
            query = f"""
            SELECT * EXCEPT(backup_timestamp)
            FROM `{backup_table_ref}`
            ORDER BY backup_timestamp DESC
            LIMIT 1
            """
            backup_data = client.query(query).to_dataframe()
            
            # Clear and restore main table
            client.query(f"TRUNCATE TABLE `{table_id}`").result()
            client.load_table_from_dataframe(
                backup_data,
                table_id,
                job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
            ).result()
            st.success("♻️ Data successfully restored from backup!")
            
        except Exception as restore_error:
            st.error(f"🔥 CRITICAL: Restoration failed - {str(restore_error)}")
            st.error("Manual intervention required. Check the backups_master table.")


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

def get_user_is_editing():
    query = f"""
        SELECT user
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
            return row.user 

    except Exception as e:
        return None

def update_is_editing(new_value: bool, user_email: str = None):
    # Consulta SQL para actualizar ambas columnas
    if user_email is None:
        user_email = st.experimental_user.email
    
    query = f"""
    UPDATE `{is_editing_table_ref}`
    SET 
        is_editing = @new_value,
        user = @user_email
    WHERE TRUE  -- Actualiza todas las filas
    """

    # Configuramos los parámetros de la consulta
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("new_value", "BOOL", new_value),
            bigquery.ScalarQueryParameter("user_email", "STRING", user_email)
        ]
    )

    try:
        # Ejecutar la consulta
        client.query(query, job_config=job_config).result()
        print("Tabla actualizada correctamente.")
    except Exception as e:
        print(f"Error updating: {e}")


def active_dfa():
    return st.session_state["dfa"][st.session_state["dfa"]["Active"] == True].copy()


def get_index(row):
    return active_dfa().iloc[row].name


def commit():
    for row in st.session_state.editor["edited_rows"]:
        row_index = get_index(row)
        for key, value in st.session_state.editor["edited_rows"][row].items():
            st.session_state["dfa"].at[row_index, key] = value
            st.session_state["dfa"].at[row_index, "id"] = f"{st.experimental_user.email}.utc.{datetime.now(timezone.utc).isoformat()}"


'''
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

'''
CREATE OR REPLACE TABLE `circular-cubist-455115-m2.app_source_data.is_editing` (
  is_editing BOOL,
  user STRING
);
'''

'''
-- TABLA PRINCIPAL DE BACKUPS (VERSIÓN MINIMALISTA)
CREATE OR REPLACE TABLE `circular-cubist-455115-m2.app_source_data.backups_master` (
  -- 1. Todas las columnas ORIGINALES (misma estructura que app_source_data)
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
  appointments INT64,
  
  -- 2. Solo un campo adicional METADATO ESENCIAL:
  backup_timestamp TIMESTAMP NOT NULL  -- Momento exacto del backup (UTC con microsegundos)
)
PARTITION BY DATE(backup_timestamp)  -- Particionado diario automático
OPTIONS (
  description = 'Copia exacta de app_source_data con timestamp de backup',
  partition_expiration_days = 365  -- Retención automática (ajustable)
);
'''

'''
# Función vieja pero funciona bien

def df_to_bq_safe(edited_df: pd.DataFrame, table_id: str = source_data_table_ref):
    """
    Safely updates a BigQuery table with automatic backup and recovery features.
    
    Args:
        table_id (str): Full BigQuery table ID (format: 'project_id.dataset_id.table_name')
        edited_df (pd.DataFrame): Edited DataFrame from Streamlit
    """
    try:
        # 1- Extract project, dataset, and table name from table_id
        project_id, dataset_id, table_name = table_id.split('.')
        
        # 2- Create a clean backup name starting with "backup_"
        clean_email = st.experimental_user.email.split('@')[0].replace('.', '_').replace('-', '_')
        
        # Usar hora UTC en formato ISO 8601 para consistencia global
        timestamp = pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%dT%H-%M-%SZ')  # Usamos guiones en lugar de : para compatibilidad con nombres de tabla
        
        backup_table_name = (
            f"{project_id}.{dataset_id}.backup_{table_name}_"
            f"{clean_email}_{timestamp}"
        )
        
        # 3- Create complete backup of original table
        st.info("🔄 Creating backup...")
        backup_job = client.query(f"CREATE TABLE `{backup_table_name}` AS SELECT * FROM `{table_id}`")
        backup_job.result()  # Wait for completion
        st.success(f"✅ Backup created: `{backup_table_name}`")
        
        # 4- Clear existing data from table
        st.info("🗑️ Deleting old data...")
        client.query(f"TRUNCATE TABLE `{table_id}`").result()
        st.success("✅ Old data deleted")
        
        # 5- Process DataFrame and upload to BigQuery
        # Remove 'Active' column if exists
        edited_df = edited_df.loc[:, edited_df.columns != "Active"]
        
        # Standardize column names
        edited_df = edited_df.rename(
            columns={
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
        
        # Upload processed data
        st.info("⬆️ Uploading new data...")
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND",
            schema_update_options=bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
        )
        upload_job = client.load_table_from_dataframe(edited_df, table_id, job_config=job_config)
        upload_job.result()
        
        # 6- Verify record count matches
        new_count = client.query(f"SELECT COUNT(*) FROM `{table_id}`").result().to_dataframe().iloc[0, 0]
        if new_count == len(edited_df):
            st.success("🎉 Database updated successfully!")
            # Optional: Uncomment to delete backup after successful update
            # client.delete_table(backup_table_name, not_found_ok=True)
        else:
            raise Exception("❌ Record count mismatch")
            
    except Exception as e:
        # 7- ERROR HANDLING: Restore from backup
        st.error(f"🚨 Error: {str(e)}")
        st.warning("🔙 Attempting to restore from backup...")
        
        try:
            # Clear potentially corrupted table
            client.query(f"TRUNCATE TABLE `{table_id}`").result()
            
            # Restore data from backup
            client.query(f"INSERT INTO `{table_id}` SELECT * FROM `{backup_table_name}`").result()
            st.success("♻️ Original data successfully restored!")
            
            # Delete the backup after restoration
            client.delete_table(backup_table_name, not_found_ok=True)
            
        except Exception as restore_error:
            st.error(f"🔥 CRITICAL: Restoration failed - {str(restore_error)}")
            st.error(f"Manual intervention required. Backup exists at: {backup_table_name}")

'''
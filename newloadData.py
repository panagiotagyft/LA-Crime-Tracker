import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime

# Replace with your actual database details
DB_HOST = 'localhost'
DB_NAME = 'LA_Crimes'
DB_USER = 'postgres'
DB_PASS = '123098giota'
CSV_FILE_PATH = 'Crime_Data_from_2020_to_Present_20241112.csv'
SQL_FILE_PATH = 'create_tables.sql'

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cursor = conn.cursor()

# Read the SQL file and execute its commands to create tables
# with open(SQL_FILE_PATH, 'r') as f:
#     sql_commands = f.read()
#     cursor.execute(sql_commands)
#     conn.commit()
# print("Tables created successfully.")

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(CSV_FILE_PATH)
print("Data loaded into DataFrame.")
print(df.info())

# Parsing helper functions
def parse_date(date_str):
    return pd.to_datetime(date_str, errors='coerce').date()

def parse_time(time_val):
    try:
        time_str = f"{int(time_val):04d}"
        return datetime.strptime(time_str, '%H%M').time()
    except:
        return None

# Preprocess the DataFrame
df['Date Rptd'] = df['Date Rptd'].apply(parse_date)
df['DATE OCC'] = df['DATE OCC'].apply(parse_date)
df['TIME OCC'] = df['TIME OCC'].apply(parse_time)

# Insert data into the `area` table
area_df = df[['AREA', 'AREA NAME']].drop_duplicates().rename(columns={'AREA': 'area_id', 'AREA NAME': 'area_name'})
area_records = area_df.to_dict('records')
execute_batch(cursor, """
    INSERT INTO Area (area_id, area_name)
    VALUES (%(area_id)s, %(area_name)s)
    ON CONFLICT (area_id) DO NOTHING
""", area_records)
print("Data inserted into `area` table.")

# Insert data into the `crime_location` table
location_df = df[['LOCATION', 'LAT', 'LON', 'Cross Street']].drop_duplicates().rename(
    columns={'LOCATION': 'location', 'LAT': 'lat', 'LON': 'lon', 'Cross Street': 'cross_street'}
)
location_records = location_df.to_dict('records')
execute_batch(cursor, """
    INSERT INTO Crime_location (location, lat, lon, cross_street)
    VALUES (%(location)s, %(lat)s, %(lon)s, %(cross_street)s)
    ON CONFLICT (location) DO NOTHING
""", location_records)
print("Data inserted into `crime_location` table.")

# Insert data into the `status` table
status_df = df[['Status', 'Status Desc']].drop_duplicates().rename(columns={'Status': 'status_code', 'Status Desc': 'status_desc'})
status_records = status_df.to_dict('records')
execute_batch(cursor, """
    INSERT INTO Status (status_code, status_desc)
    VALUES (%(status_code)s, %(status_desc)s)
    ON CONFLICT (status_code) DO NOTHING
""", status_records)
print("Data inserted into `status` table.")

# Insert data into the `premises` table
premises_df = df[['Premis Cd', 'Premis Desc']].drop_duplicates().rename(columns={'Premis Cd': 'premis_cd', 'Premis Desc': 'premis_desc'})
premises_records = premises_df.to_dict('records')
execute_batch(cursor, """
    INSERT INTO Premises (premis_cd, premis_desc)
    VALUES (%(premis_cd)s, %(premis_desc)s)
    ON CONFLICT (premis_cd) DO NOTHING
""", premises_records)
print("Data inserted into `premises` table.")

# Insert data into the `reporting_districts` table
reporting_districts_df = df[['Rpt Dist No', 'AREA']].drop_duplicates().rename(columns={'Rpt Dist No': 'rpt_dist_no', 'AREA': 'area_id'})
reporting_districts_records = reporting_districts_df.to_dict('records')
execute_batch(cursor, """
    INSERT INTO Reporting_district (rpt_dist_no, area_id)
    VALUES (%(rpt_dist_no)s, %(area_id)s)
    ON CONFLICT (rpt_dist_no) DO NOTHING
""", reporting_districts_records)
print("Data inserted into `reporting_districts` table.")

# Insert data into the `weapon` table
weapon_df = df[['Weapon Used Cd', 'Weapon Desc']].dropna().drop_duplicates().rename(columns={'Weapon Used Cd': 'weapon_cd', 'Weapon Desc': 'weapon_desc'})
weapon_records = weapon_df.to_dict('records')
execute_batch(cursor, """
    INSERT INTO weapon (weapon_cd, weapon_desc)
    VALUES (%(weapon_cd)s, %(weapon_desc)s)
    ON CONFLICT (weapon_cd) DO NOTHING
""", weapon_records)
print("Data inserted into `weapon` table.")

# Insert data into the `crime_code` table
crime_code_df = df[['Crm Cd', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4', 'Crm Cd Desc']].drop_duplicates().rename(
    columns={'Crm Cd': 'crm_cd', 'Crm Cd 2': 'crm_cd_2', 'Crm Cd 3': 'crm_cd_3', 'Crm Cd 4': 'crm_cd_4', 'Crm Cd Desc': 'crm_cd_desc'}
)
crime_code_records = crime_code_df.to_dict('records')
execute_batch(cursor, """
    INSERT INTO Crime_code (crm_cd, crm_cd_2, crm_cd_3, crm_cd_4, crm_cd_desc)
    VALUES (%(crm_cd)s, %(crm_cd_2)s, %(crm_cd_3)s, %(crm_cd_4)s, %(crm_cd_desc)s)
    ON CONFLICT (crm_cd, crm_cd_2, crm_cd_3, crm_cd_4) DO NOTHING
""", crime_code_records)
print("Data inserted into `crime_code` table.")

# Insert data into the `crime_report` table
crime_report_df = df[['DR_NO', 'Date Rptd', 'DATE OCC', 'TIME OCC', 'Status', 'Premis Cd', 'Rpt Dist No', 'AREA', 'LOCATION', 'Mocodes', 'Crm Cd', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4']].rename(columns={
    'DR_NO': 'dr_no', 'Date Rptd': 'date_rptd', 'DATE OCC': 'date_occ', 'TIME OCC': 'time_occ',
    'Status': 'status_code', 'Premis Cd': 'premis_cd', 'Rpt Dist No': 'rpt_dist_no', 'AREA': 'area_id',
    'LOCATION': 'location_id', 'Mocodes': 'mocodes', 'Crm Cd': 'crime_code_crm_cd',
    'Crm Cd 2': 'crime_code_crm_cd_2', 'Crm Cd 3': 'crime_code_crm_cd_3', 'Crm Cd 4': 'crime_code_crm_cd_4'
})
crime_report_records = crime_report_df.to_dict('records')
execute_batch(cursor, """
    INSERT INTO Crime_report (dr_no, date_rptd, date_occ, time_occ, status_code, premis_cd, rpt_dist_no, area_id, location_id, mocodes, crime_code_crm_cd, crime_code_crm_cd_2, crime_code_crm_cd_3, crime_code_crm_cd_4)
    VALUES (%(dr_no)s, %(date_rptd)s, %(date_occ)s, %(time_occ)s, %(status_code)s, %(premis_cd)s, %(rpt_dist_no)s, %(area_id)s, %(location_id)s, %(mocodes)s, %(crime_code_crm_cd)s, %(crime_code_crm_cd_2)s, %(crime_code_crm_cd_3)s, %(crime_code_crm_cd_4)s)
    ON CONFLICT (dr_no) DO NOTHING
""", crime_report_records)
print("Data inserted into `crime_report` table.")

# Insert data into the `victim` table
victim_df = df[['DR_NO', 'Vict Age', 'Vict Sex', 'Vict Descent']].rename(
    columns={'DR_NO': 'dr_no', 'Vict Age': 'vict_age', 'Vict Sex': 'vict_sex', 'Vict Descent': 'vict_descent'}
)
victim_records = victim_df.to_dict('records')
execute_batch(cursor, """
    INSERT INTO Victim (dr_no, vict_age, vict_sex, vict_descent)
    VALUES (%(dr_no)s, %(vict_age)s, %(vict_sex)s, %(vict_descent)s)
    ON CONFLICT DO NOTHING
""", victim_records)
print("Data inserted into `victim` table.")

# Commit the transaction and close the connection
conn.commit()
cursor.close()
conn.close()

print("All data successfully loaded.")

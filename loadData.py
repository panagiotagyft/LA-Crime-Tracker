import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime

# Replace with your actual details
DB_HOST = 'localhost'
DB_NAME = 'LA-Crimes'
DB_USER = 'postgres'
DB_PASS = '123098giota'
CSV_FILE_PATH = 'Crime_Data_from_2020_to_Present_20241102.csv'

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cursor = conn.cursor()

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(CSV_FILE_PATH)

# Functions for parsing dates and times
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

# Set the schema
schema = 'la_crimes'

# Insert data into the 'area' table
area_df = df[['AREA', 'AREA NAME']].drop_duplicates().rename(columns={'AREA': 'area_id', 'AREA NAME': 'area_name'})
area_records = area_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO {schema}.area (area_id, area_name)
    VALUES (%(area_id)s, %(area_name)s)
    ON CONFLICT (area_id) DO NOTHING
""", area_records)
print('ok for area!')

# Insert data into the 'status' table
status_df = df[['Status', 'Status Desc']].drop_duplicates().rename(columns={'Status': 'status', 'Status Desc': 'status_desc'})
status_records = status_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO {schema}.status (status, status_desc)
    VALUES (%(status)s, %(status_desc)s)
    ON CONFLICT (status) DO NOTHING
""", status_records)
print('ok for status!')

# Insert data into the 'premises' table
premises_df = df[['Premis Cd', 'Premis Desc']].drop_duplicates().rename(columns={'Premis Cd': 'premis_cd', 'Premis Desc': 'premis_desc'})
premises_df['premis_cd'] = premises_df['premis_cd'].fillna(-1).astype(int)
premises_records = premises_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO {schema}.premises (premis_cd, premis_desc)
    VALUES (%(premis_cd)s, %(premis_desc)s)
    ON CONFLICT (premis_cd) DO NOTHING
""", premises_records)
print('ok for premises!')

# Insert data into the 'weapon' table
weapon_df = df[['Weapon Used Cd', 'Weapon Desc']].dropna(subset=['Weapon Used Cd']).drop_duplicates().rename(
    columns={'Weapon Used Cd': 'weapon_used_cd', 'Weapon Desc': 'weapon_desc'}
)
weapon_df['weapon_used_cd'] = weapon_df['weapon_used_cd'].astype(int)
weapon_records = weapon_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO {schema}.weapon (weapon_used_cd, weapon_desc)
    VALUES (%(weapon_used_cd)s, %(weapon_desc)s)
    ON CONFLICT (weapon_used_cd) DO NOTHING
""", weapon_records)
print('ok for weapon!')

# Insert data into the 'crime_type' table
crime_type_df = df[['Crm Cd', 'Crm Cd Desc', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4']].drop_duplicates().rename(
    columns={
        'Crm Cd': 'crm_cd',
        'Crm Cd Desc': 'crm_cd_desc',
        'Crm Cd 2': 'crm_cd_2',
        'Crm Cd 3': 'crm_cd_3',
        'Crm Cd 4': 'crm_cd_4'
    }
)
# Convert data types and fill NaN with -1
crime_type_df['crm_cd'] = crime_type_df['crm_cd'].astype(int)
crime_type_df['crm_cd_2'] = crime_type_df['crm_cd_2'].fillna(-1).astype(int)
crime_type_df['crm_cd_3'] = crime_type_df['crm_cd_3'].fillna(-1).astype(int)
crime_type_df['crm_cd_4'] = crime_type_df['crm_cd_4'].fillna(-1).astype(int)
crime_type_records = crime_type_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO {schema}.crime_type (crm_cd, crm_cd_desc, crm_cd_2, crm_cd_3, crm_cd_4)
    VALUES (%(crm_cd)s, %(crm_cd_desc)s, %(crm_cd_2)s, %(crm_cd_3)s, %(crm_cd_4)s)
    ON CONFLICT (crm_cd, crm_cd_2, crm_cd_3, crm_cd_4) DO NOTHING
""", crime_type_records)
print('ok for crime_type!')

# Insert data into the 'reporting_district' table
reporting_district_df = df[['Rpt Dist No', 'AREA']].drop_duplicates().rename(
    columns={'Rpt Dist No': 'rpt_dist_no', 'AREA': 'area_area_id'}
)
reporting_district_records = reporting_district_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO {schema}.reporting_district (rpt_dist_no, area_area_id)
    VALUES (%(rpt_dist_no)s, %(area_area_id)s)
    ON CONFLICT (rpt_dist_no) DO NOTHING
""", reporting_district_records)
print('ok for reporting_district!')

# Insert data into the 'crime_location' table
location_df = df[['LOCATION', 'LAT', 'LON', 'Cross Street']].drop_duplicates().rename(
    columns={'LOCATION': 'location', 'LAT': 'lat', 'LON': 'lon', 'Cross Street': 'cross_street'}
)
location_records = location_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO {schema}.crime_location (location, lat, lon, cross_street)
    VALUES (%(location)s, %(lat)s, %(lon)s, %(cross_street)s)
    ON CONFLICT (location) DO NOTHING
""", location_records)
print('ok for crime_location!')

# Insert data into 'crime_chronicle' table
chronicle_df = df[['DATE OCC', 'TIME OCC']].drop_duplicates().rename(
    columns={'DATE OCC': 'date_occ', 'TIME OCC': 'time_occ'}
)
chronicle_records = chronicle_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO {schema}.crime_chronicle (date_occ, time_occ)
    VALUES (%(date_occ)s, %(time_occ)s)
    ON CONFLICT (date_occ, time_occ) DO NOTHING
""", chronicle_records)
print('ok for crime_chronicle!')

# Prepare and insert data into the 'crime_report' table
crime_report_df = df[['DR_NO',
                      'Date Rptd',
                      'DATE OCC',
                      'TIME OCC',
                      'Status',
                      'Premis Cd',
                      'Rpt Dist No',
                      'AREA',
                      'LOCATION',
                      'Mocodes',
                      'Crm Cd',
                      'Crm Cd 2',
                      'Crm Cd 3',
                      'Crm Cd 4']].rename(columns={
                          'DR_NO': 'dr_no',
                          'Date Rptd': 'date_rptd',
                          'DATE OCC': 'crime_chronicle_date_occ',
                          'TIME OCC': 'crime_chronicle_time_occ',
                          'Status': 'status_status',
                          'Premis Cd': 'premises_premis_cd',
                          'Rpt Dist No': 'reporting_district_rpt_dist_no',
                          'AREA': 'area_area_id',
                          'LOCATION': 'crime_location_location',
                          'Mocodes': 'mocodes',
                          'Crm Cd': 'crime_type_crm_cd',
                          'Crm Cd 2': 'crime_type_crm_cd_2',
                          'Crm Cd 3': 'crime_type_crm_cd_3',
                          'Crm Cd 4': 'crime_type_crm_cd_4'
                      })
# Fill NaN values and convert types
crime_report_df['premises_premis_cd'] = crime_report_df['premises_premis_cd'].fillna(-1).astype(int)
crime_report_df['crime_type_crm_cd'] = crime_report_df['crime_type_crm_cd'].astype(int)
crime_report_df['crime_type_crm_cd_2'] = crime_report_df['crime_type_crm_cd_2'].fillna(-1).astype(int)
crime_report_df['crime_type_crm_cd_3'] = crime_report_df['crime_type_crm_cd_3'].fillna(-1).astype(int)
crime_report_df['crime_type_crm_cd_4'] = crime_report_df['crime_type_crm_cd_4'].fillna(-1).astype(int)
crime_report_df['mocodes'] = crime_report_df['mocodes'].fillna('').astype(str)
crime_report_records = crime_report_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO {schema}.crime_report (
        dr_no,
        date_rptd,
        crime_chronicle_date_occ,
        crime_chronicle_time_occ,
        status_status,
        premises_premis_cd,
        reporting_district_rpt_dist_no,
        area_area_id,
        crime_location_location,
        mocodes,
        crime_type_crm_cd,
        crime_type_crm_cd_2,
        crime_type_crm_cd_3,
        crime_type_crm_cd_4
    )
    VALUES (
        %(dr_no)s,
        %(date_rptd)s,
        %(crime_chronicle_date_occ)s,
        %(crime_chronicle_time_occ)s,
        %(status_status)s,
        %(premises_premis_cd)s,
        %(reporting_district_rpt_dist_no)s,
        %(area_area_id)s,
        %(crime_location_location)s,
        %(mocodes)s,
        %(crime_type_crm_cd)s,
        %(crime_type_crm_cd_2)s,
        %(crime_type_crm_cd_3)s,
        %(crime_type_crm_cd_4)s
    )
    ON CONFLICT (dr_no) DO NOTHING
""", crime_report_records)
print('ok for crime_report!')

# Insert data into the 'victim' table
victim_df = df[['DR_NO', 'Vict Age', 'Vict Sex', 'Vict Descent']].drop_duplicates().rename(
    columns={'DR_NO': 'dr_no', 'Vict Age': 'vict_age', 'Vict Sex': 'vict_sex', 'Vict Descent': 'vict_descent'}
)
victim_records = victim_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO {schema}.victim (dr_no, vict_age, vict_sex, vict_descent)
    VALUES (%(dr_no)s, %(vict_age)s, %(vict_sex)s, %(vict_descent)s)
    ON CONFLICT DO NOTHING
""", victim_records)
print('ok for victim!')

# Insert data into the 'crime_report_has_weapon' table
weapons_used_df = df[['DR_NO', 'Weapon Used Cd']].dropna(subset=['Weapon Used Cd']).rename(
    columns={'DR_NO': 'crime_report_dr_no', 'Weapon Used Cd': 'weapon_weapon_used_cd'}
)
weapons_used_df['weapon_weapon_used_cd'] = weapons_used_df['weapon_weapon_used_cd'].astype(int)
weapons_used_records = weapons_used_df.drop_duplicates().to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO {schema}.crime_report_has_weapon (crime_report_dr_no, weapon_weapon_used_cd)
    VALUES (%(crime_report_dr_no)s, %(weapon_weapon_used_cd)s)
    ON CONFLICT DO NOTHING
""", weapons_used_records)
print('ok for crime_report_has_weapon!')

# Finalize transactions and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data successfully loaded into the database.")

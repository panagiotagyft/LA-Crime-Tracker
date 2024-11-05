import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime

# Replace with your actual details
DB_HOST = 'localhost'
# DB_HOST = '0.0.0.0'
DB_NAME = 'LA_Crimes'
DB_USER = 'postgres'
DB_PASS = 'example'
CSV_FILE_PATH = 'Crime_Data_from_2020_to_Present_20241105.csv'
sql_file_path = 'create_tables.sql' # Good practice to keep SQL queries in a separate file

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
print(df.head())
# exit()

print("Df size: ", df.shape)
print("Df columns: ", df.columns)
print("Df info: ", df.info())
print("Df describe: ", df.describe())
print("Df isnull: ", df.isnull().sum())

try:
    # Connect to PostgreSQL
    cur = cursor

    # Read and execute SQL file
    with open(sql_file_path, 'r') as f:
        sql_commands = f.read()
        cur.execute(sql_commands)
        conn.commit()
    
    print("Tables created successfully.")

    # Close the cursor and connection
    cur.close()
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")
    
print("Tables created successfully.")



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
print("ok for preprocessing date")
df['DATE OCC'] = df['DATE OCC'].apply(parse_date)
# df['TIME OCC'] = df['TIME OCC'].apply(parse_time)
print("ok for preprocessing date oc")
# Insert data into the 'area' table
area_df = df[['AREA', 'AREA NAME']].rename(columns={'AREA': 'area_id', 'AREA NAME': 'area_name'})
area_records = area_df.drop_duplicates(subset=['area_id']).to_dict('records')
print("drop duplicates")
execute_batch(cursor, """
    INSERT INTO area (area_id, area_name)
    VALUES (%s, %s)
    ON CONFLICT (area_id) DO NOTHING
""", [(record['area_id'], record['area_name']) for record in area_records])
print('ok for area!')

# Insert data into the 'status' table
status_df = df[['Status', 'Status Desc']].rename(columns={'Status': 'status', 'Status Desc': 'status_desc'})
status_records = status_df.drop_duplicates(subset=['status']).to_dict('records')
execute_batch(cursor, """
    INSERT INTO status (status, status_desc)
    VALUES (%s, %s)
    ON CONFLICT (status) DO NOTHING
""", [(record['status'], record['status_desc']) for record in status_records])
print('ok for status!')

# Insert data into the 'premises' table
premises_df = df[['Premis Cd', 'Premis Desc']].rename(columns={'Premis Cd': 'premis_cd', 'Premis Desc': 'premis_desc'})
premises_df['premis_cd'] = premises_df['premis_cd'].fillna(-1).astype(int)
premises_records = premises_df.drop_duplicates(subset=['premis_cd']).to_dict('records')
execute_batch(cursor, """
    INSERT INTO premises (premis_cd, premis_desc)
    VALUES (%s, %s)
    ON CONFLICT (premis_cd) DO NOTHING
""", [(record['premis_cd'], record['premis_desc']) for record in premises_records])
print('ok for premises!')

# Insert data into the 'weapon' table
weapon_df = df[['Weapon Used Cd', 'Weapon Desc']].dropna(subset=['Weapon Used Cd']).rename(
    columns={'Weapon Used Cd': 'weapon_used_cd', 'Weapon Desc': 'weapon_desc'}
)
records = weapon_df.drop_duplicates(subset=['weapon_used_cd']).to_dict('records')
execute_batch(cursor, """
    INSERT INTO weapon (weapon_used_cd, weapon_desc)
    VALUES (%s, %s)
    ON CONFLICT (weapon_used_cd) DO NOTHING
""", [(record['weapon_used_cd'], record['weapon_desc']) for record in records])
print('ok for weapon!')

# Insert data into the 'crime_type' table
crime_type_df = df[['Crm Cd', 'Crm Cd Desc', 'Mocodes', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4']].rename(
    columns={
        'Crm Cd': 'crm_cd',
        'Crm Cd Desc': 'crm_cd_desc',
        'Mocodes': 'mocodes',
        'Crm Cd 2': 'crm_cd_2',
        'Crm Cd 3': 'crm_cd_3',
        'Crm Cd 4': 'crm_cd_4'
    }
)
# Convert data types to numeric
crime_type_df['crm_cd'] = crime_type_df['crm_cd'].astype('Int64')
crime_type_df['crm_cd_2'] = crime_type_df['crm_cd_2'].astype('Int64')
crime_type_df['crm_cd_3'] = crime_type_df['crm_cd_3'].astype('Int64')
crime_type_df['crm_cd_4'] = crime_type_df['crm_cd_4'].astype('Int64')
crime_type_records = crime_type_df.drop_duplicates(subset=['crm_cd']).to_dict('records')
execute_batch(cursor, """
    INSERT INTO crime_type (crm_cd, crm_cd_desc, mocodes, crm_cd_2, crm_cd_3, crm_cd_4)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (crm_cd) DO NOTHING
""", [(record['crm_cd'], record['crm_cd_desc'], record['mocodes'], record['crm_cd_2'],
       record['crm_cd_3'], record['crm_cd_4']) for record in crime_type_records])
print('ok for crime_type!')

# Insert data into the 'reporting_district' table
reporting_district_df = df[['Rpt Dist No', 'AREA']].rename(
    columns={'Rpt Dist No': 'rpt_dist_no', 'AREA': 'area_area_id'}
)
reporting_district_records = reporting_district_df.drop_duplicates(subset=['rpt_dist_no', 'area_area_id']).to_dict('records')
execute_batch(cursor, """
    INSERT INTO reporting_district (rpt_dist_no, area_area_id)
    VALUES (%s, %s)
    ON CONFLICT (rpt_dist_no) DO NOTHING
""", [(record['rpt_dist_no'], record['area_area_id']) for record in reporting_district_records])
print('ok for reporting_district!')

# Insert data into the 'crime_location' table and retrieve 'location_id'
location_df = df[['LOCATION', 'LAT', 'LON', 'Cross Street']].rename(
    columns={'LOCATION': 'location', 'LAT': 'lat', 'LON': 'lon', 'Cross Street': 'cross_street'}
)
location_records = location_df.drop_duplicates(subset=['location', 'lat', 'lon', 'cross_street']).to_dict('records')

for record in location_records:
    cursor.execute("""
        INSERT INTO crime_location (location, lat, lon, cross_street)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (location) DO NOTHING
    """, (record['location'], record['lat'], record['lon'], record['cross_street']))
print('ok for crime_location!')

# Insert data into 'crime_chronicle' table
chronicle_df = df[['DATE OCC', 'TIME OCC']].rename(columns={'DATE OCC': 'date_occ', 'TIME OCC': 'time_occ'})
chronicle_df = chronicle_df.drop_duplicates()
chronicle_records = chronicle_df.to_dict('records')
execute_batch(cursor, """
    INSERT INTO crime_chronicle (date_occ, time_occ)
    VALUES (%s, %s)
    ON CONFLICT DO NOTHING
""", [(record['date_occ'], record['time_occ']) for record in chronicle_records])
print('ok for crime_chronicle!')

# Prepare and insert data into the 'crime_report' table
crime_df = df[['DR_NO', 
               'Date Rptd', 
               'DATE OCC', 
               'TIME OCC', 
               'Status', 
               'Premis Cd', 
               'Rpt Dist No', 
               'AREA', 
               'LOCATION']].rename(columns={'DR_NO': 'dr_no', 
                                            'Date Rptd': 'date_rptd',
                                            'DATE OCC': 'date_occ',
                                            'TIME OCC': 'time_occ',
                                            'Status': 'status',
                                            'Premis Cd': 'premis_cd',
                                            'Rpt Dist No': 'rpt_dist_no',
                                            'AREA': 'area_id',
                                            'LOCATION': 'location'})

crime_df['premis_cd'] = crime_df['premis_cd'].fillna(-1).astype(int)
crime_records = crime_df.to_dict('records')

execute_batch(cursor, """
    INSERT INTO crime_report (
        dr_no, date_rptd, crime_chronicle_date_occ, crime_chronicle_time_occ, status_status,
        premises_premis_cd, reporting_district_rpt_dist_no,
        area_area_id, crime_location_location
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (dr_no) DO NOTHING
""", [(record['dr_no'], 
       record['date_rptd'], 
       record['date_occ'], 
       record['time_occ'], 
       record['status'], 
       record['premis_cd'], 
       record['rpt_dist_no'], 
       record['area_id'], 
       record['location'],) for record in crime_records])
print('ok for crime_report!')

# Insert data into the 'victim' table
victim_df = df[['DR_NO', 'Vict Age', 'Vict Sex', 'Vict Descent']].rename(
    columns={'DR_NO': 'dr_no', 'Vict Age': 'vict_age', 'Vict Sex': 'vict_sex', 'Vict Descent': 'vict_descent'}
)
victim_records = victim_df.to_dict('records')

execute_batch(cursor, """
    INSERT INTO victim (dr_no, vict_age, vict_sex, vict_descent)
    VALUES (%(dr_no)s, %(vict_age)s, %(vict_sex)s, %(vict_descent)s)
    ON CONFLICT DO NOTHING
""", victim_records)
print('ok for victim!')

crime_codes = []
for idx, row in df.iterrows():
    crime_codes.append((
        row['DR_NO'],
        row['Crm Cd'],
    ))

execute_batch(cursor, """
    INSERT INTO crime_incident_crime_code (dr_no, crm_cd)
    VALUES (%s, %s)
    ON CONFLICT DO NOTHING
""", crime_codes)
print('ok for crime_incident_crime_code!')

# Insert data into the 'crime_report_has_weapon' table
weapons_used = df[['DR_NO', 'Weapon Used Cd']].dropna(subset=['Weapon Used Cd'])

# Convert the DataFrame to a list of tuples
weapons_used_records = weapons_used.values.tolist()

execute_batch(cursor, """
    INSERT INTO crime_report_has_weapon (crime_report_dr_no, weapon_weapon_used_cd)
    VALUES (%s, %s)
    ON CONFLICT DO NOTHING
""", weapons_used_records)
print('ok for crime_report_has_weapon!')

# Finalize transactions and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data successfully loaded into the database.")

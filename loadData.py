import pandas as pd 
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime

# Replace with your actual details
DB_HOST = '127.0.0.1'
DB_NAME = 'crime_tracker'
DB_USER = 'crime_user'
DB_PASS = '123098giota'
CSV_FILE_PATH = 'Crime_Data_from_2020_to_Present_20241102.csv'
sql_commands = 'create_tables.sql'

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cursor = conn.cursor()

# Drop all tables in the public schema
drop_all_tables_query = """
DO $$ 
DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;
"""

cursor.execute(drop_all_tables_query)
conn.commit()

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(CSV_FILE_PATH)

try:
    # Connect to PostgreSQL
    cur = cursor
    # Read and execute SQL file
    with open(sql_commands, 'r') as f:
        sql_commands = f.read()
        cur.execute(sql_commands)
        conn.commit()
    
    print("Tables created successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

# Query to fetch tables and their columns
query = """
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
"""

cursor.execute(query)

# Print tables and columns
current_table = None
for table_name, column_name, data_type in cursor.fetchall():
    if table_name != current_table:
        print(f"\nTable: {table_name}")
        current_table = table_name
    print(f"  Column: {column_name} ({data_type})")

print("Tables created successfully.")

# ---------------------------------------------------------------------
# -------------------------    Load Data    ---------------------------
# ---------------------------------------------------------------------

# Functions for parsing dates and times
def parse_date(date_str):
    return pd.to_datetime(date_str, errors='coerce').date()

def parse_time(time_val):
    try:
        time_str = f"{int(time_val):04d}"
        return datetime.strptime(time_str, '%H%M').time()
    except:
        return None
    
df['Date Rptd'] = df['Date Rptd'].apply(parse_date)
df['DATE OCC'] = df['DATE OCC'].apply(parse_date)
df['TIME OCC'] = df['TIME OCC'].apply(parse_time)

# ---------------------------------------------------------------------
# Insert data into the -- Area -- table
area_df = df[['AREA', 'AREA NAME']].rename(columns={'AREA': 'area_id', 'AREA NAME': 'area_name'})
area_records = area_df.drop_duplicates(subset=['area_id']).to_dict('records')
execute_batch(cursor, """
    INSERT INTO Area (area_id, area_name)
    VALUES (%s, %s)
    ON CONFLICT (area_id) DO NOTHING
""", [(record['area_id'], record['area_name']) for record in area_records])
conn.commit()
print('ok for Area!')

# ---------------------------------------------------------------------
# Insert data into the -- Crime_Location -- table
# Step 1: Insert unique locations into Crime_Location
location_df = df[['LOCATION', 'LAT', 'LON', 'Cross Street']].rename(
    columns={'LOCATION': 'location', 'LAT': 'lat', 'LON': 'lon', 'Cross Street': 'cross_street'}
)

# Remove duplicates to ensure we only insert unique locations
location_records = location_df.drop_duplicates(subset=['location', 'lat', 'lon', 'cross_street']).to_dict('records')

# Insert unique locations into Crime_Location
for record in location_records:
    cursor.execute("""
        INSERT INTO Crime_Location (location, lat, lon, cross_street)
        VALUES (%s, %s, %s, %s)
    """, (record['location'], record['lat'], record['lon'], record['cross_street']))
conn.commit()  # Commit the transaction to save changes

print('ok for Crime_Location!')

# Step 2: Retrieve all location_ids with their details from Crime_Location
cursor.execute("""
    SELECT location_id, location, lat, lon, cross_street
    FROM Crime_Location
""")
location_rows = cursor.fetchall()
location_id_map = { (row[1], float(row[2]), float(row[3])): row[0] for row in location_rows }

# Add get_location_id to df
def get_location_id(row):
    key = (row['LOCATION'], float(row['LAT']), float(row['LON']))
    return location_id_map.get(key)

# Apply the mapping function to add the location_id to each row in your DataFrame
df['location_id'] = df.apply(get_location_id, axis=1)

# ---------------------------------------------------------------------
# Insert data into the -- Status -- table
# Correction: Use 'status_code' as the column name
status_df = df[['Status', 'Status Desc']].rename(columns={'Status': 'status_code', 'Status Desc': 'status_desc'})
status_records = status_df.drop_duplicates(subset=['status_code']).to_dict('records')
execute_batch(cursor, """
    INSERT INTO Status (status_code, status_desc)
    VALUES (%s, %s)
    ON CONFLICT (status_code) DO NOTHING
""", [(record['status_code'], record['status_desc']) for record in status_records])
conn.commit()
print('ok for Status!')

# ---------------------------------------------------------------------
# Insert data into the -- Premises -- table
premises_df = df[['Premis Cd', 'Premis Desc']].rename(columns={'Premis Cd': 'premis_cd', 'Premis Desc': 'premis_desc'})
premises_df['premis_cd'] = premises_df['premis_cd'].fillna(-1).astype(int)
premises_records = premises_df.drop_duplicates(subset=['premis_cd']).to_dict('records')
execute_batch(cursor, """
    INSERT INTO Premises (premis_cd, premis_desc)
    VALUES (%s, %s)
    ON CONFLICT (premis_cd) DO NOTHING
""", [(record['premis_cd'], record['premis_desc']) for record in premises_records])
conn.commit()
print('ok for Premises!')

# ---------------------------------------------------------------------
# Insert data into the -- Reporting_District -- table
reporting_district_df = df[['Rpt Dist No', 'AREA']].rename(
    columns={'Rpt Dist No': 'rpt_dist_no', 'AREA': 'area_id'}
)
# Correction: Use 'area_id' instead of 'area_area_id'
reporting_district_records = reporting_district_df.drop_duplicates(subset=['rpt_dist_no', 'area_id']).to_dict('records')
execute_batch(cursor, """
    INSERT INTO Reporting_District (rpt_dist_no, area_id)
    VALUES (%s, %s)
    ON CONFLICT (rpt_dist_no) DO NOTHING
""", [(record['rpt_dist_no'], record['area_id']) for record in reporting_district_records])
conn.commit()
print('ok for Reporting_District!')

# ---------------------------------------------------------------------
# Insert data into the -- Weapon -- table
weapon_df = df[['Weapon Used Cd', 'Weapon Desc']].rename(columns={'Weapon Used Cd': 'weapon_cd', 'Weapon Desc': 'weapon_desc'})
weapon_df['weapon_cd'] = weapon_df['weapon_cd'].fillna(-1).astype(int)
weapon_records = weapon_df.drop_duplicates(subset=['weapon_cd']).to_dict('records')
execute_batch(cursor, """
    INSERT INTO Weapon (weapon_cd, weapon_desc)
    VALUES (%(weapon_cd)s, %(weapon_desc)s)
    ON CONFLICT (weapon_cd) DO NOTHING
""", weapon_records)
conn.commit()
print('ok for Weapon!')

# ---------------------------------------------------------------------
# Insert data into the -- Crime_code -- table
# Collect all 'Crm Cd's and their descriptions
crm_code_list = []

# List to store all Crm Cd data
crm_code_list = []

# Loop through all Crm Cd {i} columns
for i in range(1, 5):
    if i == 1:
        # For i = 1, include both Crm Cd and Crm Cd Desc
        crm_cd_col = 'Crm Cd'
        crm_cd_desc_col = 'Crm Cd Desc'
        if crm_cd_col in df.columns and crm_cd_desc_col in df.columns:
            temp_df = df[[crm_cd_col, crm_cd_desc_col]].drop_duplicates()  # Remove duplicates
            temp_df.columns = ['crm_cd', 'crm_cd_desc']  # Rename columns for consistency
            crm_code_list.append(temp_df)
    else:
        # For i = 2, 3, 4, only include Crm Cd {i}
        crm_cd_col = f'Crm Cd {i}'
        if crm_cd_col in df.columns:
            temp_df = df[[crm_cd_col]].drop_duplicates()  # Remove duplicates
            temp_df.columns = ['crm_cd']  # Rename the column
            temp_df['crm_cd_desc'] = 'there is no description!'  # Add a description column with empty values
            crm_code_list.append(temp_df)  # Append to the list


crm_code_df = pd.concat(crm_code_list).drop_duplicates()
crm_code_df['crm_cd'] = crm_code_df['crm_cd'].fillna(-1).astype(int)
crm_code_records = crm_code_df.to_dict('records')

# Insert into Crime_code
execute_batch(cursor, """
    INSERT INTO Crime_code (crm_cd, crm_cd_desc)
    VALUES (%(crm_cd)s, %(crm_cd_desc)s)
""", crm_code_records)
conn.commit()
print('ok for Crime_code!')

# Retrieve mapping from crm_cd to crm_cd_id
cursor.execute("""
    SELECT crm_cd_id, crm_cd
    FROM Crime_code
""")
crm_code_rows = cursor.fetchall()
crm_cd_id_map = {row[1]: row[0] for row in crm_code_rows}
df['Crm Cd'] = df['Crm Cd'].fillna(-1).astype(int)
df['Crm Cd 2'] = df['Crm Cd 2'].fillna(-1).astype(int)
df['Crm Cd 3'] = df['Crm Cd 3'].fillna(-1).astype(int)
df['Crm Cd 4'] = df['Crm Cd 4'].fillna(-1).astype(int)
# Add crm_cd_id columns to df
df['crm_cd_id'] = df['Crm Cd'].apply(lambda x: crm_cd_id_map.get(int(x)))
df['crm_cd_2_id'] = df['Crm Cd 2'].apply(lambda x: crm_cd_id_map.get(int(x)))
df['crm_cd_3_id'] = df['Crm Cd 3'].apply(lambda x: crm_cd_id_map.get(int(x)))
df['crm_cd_4_id'] = df['Crm Cd 4'].apply(lambda x: crm_cd_id_map.get(int(x)))

# ---------------------------------------------------------------------
# Insert data into the -- Timestamp -- table
# Ensure unique combinations of date_occ and time_occ
timestamp_df = df[['DATE OCC', 'TIME OCC']].rename(columns={'DATE OCC': 'date_occ', 'TIME OCC': 'time_occ'})
timestamp_records = timestamp_df.drop_duplicates().to_dict('records')

# Insert into Timestamp
execute_batch(cursor, """
    INSERT INTO Timestamp (date_occ, time_occ)
    VALUES (%(date_occ)s, %(time_occ)s)
    ON CONFLICT DO NOTHING
""", timestamp_records)
conn.commit()
print('ok for Timestamp!')

# Retrieve mapping from (date_occ, time_occ) to timestamp_id
cursor.execute("""
    SELECT timestamp_id, date_occ, time_occ
    FROM Timestamp
""")
timestamp_rows = cursor.fetchall()
timestamp_id_map = { (row[1], row[2]): row[0] for row in timestamp_rows }

# Add timestamp_id to df
def get_timestamp_id(row):
    key = (row['DATE OCC'], row['TIME OCC'])
    return timestamp_id_map.get(key)

df['timestamp_id'] = df.apply(get_timestamp_id, axis=1)

# ---------------------------------------------------------------------
# Insert data into the -- Crime_report -- table
crime_report_df = df[['DR_NO', 'Date Rptd', 'timestamp_id', 'Status', 'Premis Cd',
                      'Rpt Dist No', 'AREA', 'location_id', 'Mocodes', 'Weapon Used Cd',
                      'crm_cd_id', 'crm_cd_2_id', 'crm_cd_3_id', 'crm_cd_4_id']].rename(
    columns={
        'DR_NO': 'dr_no',
        'Date Rptd': 'date_rptd',
        'Status': 'status_code',
        'Premis Cd': 'premis_cd',
        'Rpt Dist No': 'rpt_dist_no',
        'AREA': 'area_id',
        'Mocodes': 'mocodes',
        'Weapon Used Cd': 'weapon_cd'
    }
)
crime_report_df['premis_cd'] = crime_report_df['premis_cd'].fillna(-1).astype(int)
crime_report_df['weapon_cd'] = crime_report_df['weapon_cd'].fillna(-1).astype(int)
crime_report_df['rpt_dist_no'] = crime_report_df['rpt_dist_no'].fillna(-1).astype(int)
crime_report_records = crime_report_df.to_dict('records')

for record in crime_report_records:
    cursor.execute("""
        INSERT INTO Crime_report (
            dr_no, date_rptd, timestamp_id, status_code, premis_cd, rpt_dist_no,
            area_id, location_id, mocodes, weapon_cd, crm_cd, crm_cd_2, crm_cd_3, crm_cd_4
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        record['dr_no'],
        record['date_rptd'],
        record['timestamp_id'],
        record['status_code'],
        record['premis_cd'],
        record['rpt_dist_no'],
        record['area_id'],
        record['location_id'],
        record['mocodes'],
        record['weapon_cd'],
        record['crm_cd_id'],
        record['crm_cd_2_id'],
        record['crm_cd_3_id'],
        record['crm_cd_4_id']
    ))
conn.commit()
print('ok for Crime_report!')

# ---------------------------------------------------------------------
# Insert data into the -- Victim -- table
victim_df = df[['DR_NO', 'Vict Age', 'Vict Sex', 'Vict Descent']].rename(
    columns={'DR_NO': 'dr_no', 'Vict Age': 'vict_age', 'Vict Sex': 'vict_sex', 'Vict Descent': 'vict_descent'}
)
victim_records = victim_df.to_dict('records')

for record in victim_records:
    cursor.execute("""
        INSERT INTO Victim (
            dr_no, vict_age, vict_sex, vict_descent
        ) VALUES (%s, %s, %s, %s)
    """, (
        record['dr_no'],
        record['vict_age'],
        record['vict_sex'],
        record['vict_descent']
    ))
conn.commit()
print('ok for Victim!')

# Close the cursor and connection
cursor.close()
conn.close()

import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime

# Replace with your actual details
DB_HOST = 'localhost'
DB_NAME = 'LA_Crimes'
DB_USER = 'postgres'
DB_PASS = '123098giota'
CSV_FILE_PATH = 'Crime_Data_from_2020_to_Present_20241112_10k.csv'
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

print("Df size: ", df.shape)
print("Df columns: ", df.columns)
print("Df info: ", df.info())
print("Df describe: ", df.describe())
print("Df isnull: ", df.isnull().sum())

try:
    # Connect to PostgreSQL
    cur = cursor
    # Read and execute SQL file
    with open(sql_commands, 'r') as f:
        sql_commands = f.read()
        cur.execute(sql_commands)
        conn.commit()
    
    print("Tables created successfully.")

    # Close the cursor and connection
    # cur.close()
    # conn.close()

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
df['TIME OCC'] = df['TIME OCC'].apply(parse_time)


# Insert data into the 'area' table
area_df = df[['AREA', 'AREA NAME']].drop_duplicates().rename(columns={'AREA': 'area_id', 'AREA NAME': 'area_name'})
area_records = area_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO Area (area_id, area_name)
    VALUES (%(area_id)s, %(area_name)s)
    ON CONFLICT (area_id) DO NOTHING
""", area_records)
print('ok for area!')

# Insert data into the 'status' table
status_df = df[['Status', 'Status Desc']].drop_duplicates().rename(columns={'Status': 'status', 'Status Desc': 'status_desc'})
status_records = status_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO Status (status_code, status_desc)
    VALUES (%(status)s, %(status_desc)s)
""", status_records)
print('ok for status!')

# Insert data into the 'premises' table
premises_df = df[['Premis Cd', 'Premis Desc']].drop_duplicates().rename(columns={'Premis Cd': 'premis_cd', 'Premis Desc': 'premis_desc'})
premises_df['premis_cd'] = premises_df['premis_cd'].fillna(-1).astype(int)
premises_records = premises_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO Premises (premis_cd, premis_desc)
    VALUES (%(premis_cd)s, %(premis_desc)s)
    ON CONFLICT (premis_cd) DO NOTHING
""", premises_records)
print('ok for premises!')

# Insert data into the 'weapon' table
weapon_df = df[['Weapon Used Cd', 'Weapon Desc']].dropna(subset=['Weapon Used Cd']).drop_duplicates().rename(
    columns={'Weapon Used Cd': 'weapon_cd', 'Weapon Desc': 'weapon_desc'}
)
weapon_df['weapon_cd'] = weapon_df['weapon_cd'].astype(int)
weapon_records = weapon_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO Weapon (weapon_cd, weapon_desc)
    VALUES (%(weapon_cd)s, %(weapon_desc)s)
    ON CONFLICT (weapon_cd) DO NOTHING
""", weapon_records)
print('ok for weapon!')

# Insert data into the 'crime_type' table
crime_type_df = df[['Crm Cd', 'Crm Cd Desc']].drop_duplicates().rename(
    columns={
        'Crm Cd': 'crm_cd',
        'Crm Cd Desc': 'crm_cd_desc'
    }
)
# Convert data types and fill NaN with -1
crime_type_df['crm_cd'] = crime_type_df['crm_cd'].astype(int)
crime_type_df['crm_cd_desc'] = crime_type_df['crm_cd_desc'].fillna('').astype(str)

crime_type_records = crime_type_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO Crime_code (crm_cd, crm_cd_desc)
    VALUES (%(crm_cd)s, %(crm_cd_desc)s)
    ON CONFLICT (crm_cd) DO NOTHING
""", crime_type_records)

# Insert unique values of crm_cd_1, crm_cd_2, crm_cd_3, and crm_cd_4 with empty crime_cd_desc
unique_crm_cd = pd.concat([
    df['Crm Cd'],
    df['Crm Cd 2'],
    df['Crm Cd 3'],
    df['Crm Cd 4']
]).dropna().unique()

unique_crm_cd_df = pd.DataFrame({
    'crm_cd': unique_crm_cd,
    'crm_cd_desc': [''] * len(unique_crm_cd)  #! empty string , set on crm_cd_2/3/4
})

unique_crm_cd_records = unique_crm_cd_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO Crime_code (crm_cd, crm_cd_desc)
    VALUES (%(crm_cd)s, %(crm_cd_desc)s)
    ON CONFLICT (crm_cd) DO NOTHING
""", unique_crm_cd_records)

print('ok for crime_type!')

# Insert data into the 'reporting_district' table
reporting_district_df = df[['Rpt Dist No', 'AREA']].drop_duplicates().rename(
    columns={'Rpt Dist No': 'rpt_dist_no', 'AREA': 'area_id'}
)
reporting_district_records = reporting_district_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO Reporting_district (rpt_dist_no, area_id)
    VALUES (%(rpt_dist_no)s, %(area_id)s)
    ON CONFLICT (rpt_dist_no) DO NOTHING
""", reporting_district_records)
print('ok for reporting_district!')

# Insert data into the 'crime_location' table
location_df = df[['LOCATION', 'LAT', 'LON', 'Cross Street']].drop_duplicates().rename(
    columns={'LOCATION': 'location', 'LAT': 'lat', 'LON': 'lon', 'Cross Street': 'cross_street'}
)
location_records = location_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO Crime_location (location, lat, lon, cross_street)
    VALUES (%(location)s, %(lat)s, %(lon)s, %(cross_street)s)
""", location_records)
print('ok for crime_location!')
# Insert data into 'timestamp' table
timestamp_df = df[['DATE OCC', 'TIME OCC']].drop_duplicates().rename(
    columns={'DATE OCC': 'date_occ', 'TIME OCC': 'time_occ'}
)
timestamp_records = timestamp_df.to_dict('records')

execute_batch(cursor, f"""
    INSERT INTO Timestamp (date_occ, time_occ)
    VALUES (%(date_occ)s, %(time_occ)s)
    ON CONFLICT DO NOTHING
""", timestamp_records)

print('ok for timestamp!')



# Retrieve all timestamp_id mappings for future use
cursor.execute("SELECT timestamp_id, date_occ, time_occ FROM Timestamp")
timestamp_mappings = cursor.fetchall()

# Create a mapping dictionary for date_occ and time_occ to timestamp_id for future use
timestamp_id_map = {(row[1], row[2]): row[0] for row in timestamp_mappings}

# Prepare and insert data into the 'crime_report' table
crime_report_df = df[['DR_NO',
                      'Date Rptd',
                      'DATE OCC',
                      'TIME OCC',
                      'Status',
                      'Premis Cd',
                      'Rpt Dist No',
                      'Mocodes',
                      'Weapon Used Cd',
                      'AREA',
                      'LOCATION',
                      'LAT',
                      'LON',
                      'Cross Street',
                      'Crm Cd',
                      'Crm Cd 2',
                      'Crm Cd 3',
                      'Crm Cd 4']].rename(columns={
                          'DR_NO': 'dr_no',
                          'Date Rptd': 'date_rptd',
                          'DATE OCC': 'date_occ',
                          'TIME OCC': 'time_occ',
                          'Status': 'status_code',
                          'Premis Cd': 'premis_cd',
                          'Rpt Dist No': 'rpt_dist_no',
                          'Mocodes': 'mocodes',
                          'Weapon Used Cd': 'weapon_cd',
                          'AREA': 'area_id',
                          'LOCATION': 'location',
                          'LAT': 'lat',
                          'LON': 'lon',
                          'Cross Street': 'cross_street',
                          'Crm Cd': 'crm_cd',
                          'Crm Cd 2': 'crm_cd_2',
                          'Crm Cd 3': 'crm_cd_3',
                          'Crm Cd 4': 'crm_cd_4'
                      })

print("crime_report_df: ", crime_report_df.head(3))
exit()

# Fill NaN values and convert types
crime_report_df['premis_cd'] = crime_report_df['premis_cd'].fillna(-1).astype(int)
crime_report_df['crm_cd'] = crime_report_df['crm_cd'].astype(int)
crime_report_df['crm_cd_2'] = crime_report_df['crm_cd_2'].fillna(-1).astype(int)
crime_report_df['crm_cd_3'] = crime_report_df['crm_cd_3'].fillna(-1).astype(int)
crime_report_df['crm_cd_4'] = crime_report_df['crm_cd_4'].fillna(-1).astype(int)
crime_report_df['mocodes'] = crime_report_df['mocodes'].fillna('').astype(str)


# Add timestamp_id to the DataFrame using the mapping dictionary
crime_report_df['timestamp_id'] = crime_report_df.apply(
    lambda row: timestamp_id_map.get((row['date_occ'], row['time_occ'])),
    axis=1
)

print("crime_report_df: ", crime_report_df.head())


for i in range(0, 3):
    print("i is ", i)
    print("Crime report df dr_no: ", crime_report_df['dr_no'][i])
    print("Crime report df date_rptd: ", crime_report_df['date_rptd'][i])
    print("Crime report df timestamp_id: ", crime_report_df['timestamp_id'][i])
    print("Crime report df crm_cd: ", crime_report_df['crm_cd'][i])
    
print("crime_report_df: ", crime_report_df.head(3))



# Drop columns no longer needed
crime_report_df = crime_report_df.drop(columns=['date_occ', 'time_occ'])
#Same for location_id
cursor.execute("SELECT location_id, location, lat, lon, cross_street FROM Crime_Location")
crime_location_mappings = cursor.fetchall()
# Create a mapping dictionary for (location, lat, lon, cross_street) to location_id
crime_location_id_map = {
    (row[1], row[2], row[3], row[4]): row[0]
    for row in crime_location_mappings
}

# Add location_id to the DataFrame using the mapping dictionary
crime_report_df['location_id'] = crime_report_df.apply(
    lambda row: crime_location_id_map.get(
        (row['location'], row['lat'], row['lon'], row.get('cross_street'))
    ),
    axis=1
)

crime_report_df = crime_report_df.drop(columns=['location', 'lat', 'lon', 'cross_street'])


for i in range(0, 3):
    print("i is ", i)
    print("Crime report df dr_no: ", crime_report_df['dr_no'][i])
    print("Crime report df date_rptd: ", crime_report_df['date_rptd'][i])
    print("Crime report df timestamp_id: ", crime_report_df['timestamp_id'][i])
    print("Crime report df crm_cd: ", crime_report_df['crm_cd'][i])
    print("Crime report location_id: ", crime_report_df['location_id'][i])

print("crime_report_df: ", crime_report_df.head())

crime_report_records = crime_report_df.to_dict('records')
execute_batch(cursor, """
    INSERT INTO Crime_report (
        dr_no,
        date_rptd,
        timestamp_id,
        status_code,
        premis_cd,
        rpt_dist_no,
        area_id,
        location_id,
        mocodes,
        weapon_cd,
        crm_cd,
        crm_cd_2,
        crm_cd_3,
        crm_cd_4
    )
    VALUES (
        %(dr_no)s,
        %(date_rptd)s,
        %(timestamp_id)s,
        %(status_code)s,
        %(premis_cd)s,
        %(rpt_dist_no)s,
        %(area_id)s,
        %(location_id)s,
        %(mocodes)s,
        %(weapon_cd)s,
        %(crm_cd)s,
        %(crm_cd_2)s,
        %(crm_cd_3)s,
        %(crm_cd_4)s
    )
    ON CONFLICT DO NOTHING
""", crime_report_records)



print('ok for crime_report!')

# Insert data into the 'victim' table
victim_df = df[['DR_NO', 'Vict Age', 'Vict Sex', 'Vict Descent']].drop_duplicates().rename(
    columns={'DR_NO': 'dr_no', 'Vict Age': 'vict_age', 'Vict Sex': 'vict_sex', 'Vict Descent': 'vict_descent'}
)
victim_records = victim_df.to_dict('records')
execute_batch(cursor, f"""
    INSERT INTO Victim (dr_no, vict_age, vict_sex, vict_descent)
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
    INSERT INTO Crime_report_has_weapon (crime_report_dr_no, weapon_weapon_used_cd)
    VALUES (%(crime_report_dr_no)s, %(weapon_weapon_used_cd)s)
    ON CONFLICT DO NOTHING
""", weapons_used_records)
print('ok for crime_report_has_weapon!')

# Finalize transactions and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data successfully loaded into the database.")

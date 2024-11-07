import pandas as pd
import psycopg2

DB_HOST = 'localhost'
DB_NAME = 'LA Crimes 2'
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

# -- 2
t=2130
c=510
sql = """
    SELECT report.date_rptd, COUNT(report.dr_no)
    FROM crime_report AS report
    INNER JOIN crime_incident_crime_code AS code ON report.dr_no = code.dr_no 
    WHERE report.crime_chronicle_time_occ = %s AND code.crm_cd = %s
    GROUP BY report.date_rptd
    ORDER BY report.date_rptd;
"""

# Execute the query with parameters
cursor.execute(sql, (t, c))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]} -> {row[1]}")
print(len(results))
# Finalize transaction and close connection
cursor.close()
conn.close()
import pandas as pd
import psycopg2

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

# -- 2
t='21:30:00'
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
print()


# -- 4
start_date = '2023-01-01'
end_date =  '2023-01-31'
sql = """
SELECT count(cr.dr_no) / count(distinct cr.crime_chronicle_date_occ)
FROM crime_report AS cr 
WHERE cr.crime_chronicle_date_occ > %s and cr.crime_chronicle_date_occ < %s
"""

# Execute the query with parameters
cursor.execute(sql, (start_date, end_date))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]}")
print()

# -- 6
start_date = '2023-01-01'
end_date =  '2023-01-31'

sql="""
WITH DailyCrimeCounts AS (
    SELECT 
        area_name,
        cr.crime_chronicle_date_occ AS crime_date,
        COUNT(*) AS daily_crimes
    FROM crime_report AS cr
    INNER JOIN area ON cr.area_area_id = area.area_id
    WHERE cr.crime_chronicle_date_occ BETWEEN %s AND %s
    GROUP BY area_name, cr.crime_chronicle_date_occ 
)

SELECT 
    area_name, 
    crime_date,
    daily_crimes
FROM 
    DailyCrimeCounts
ORDER BY 
    daily_crimes DESC
LIMIT 5;
"""
cursor.execute(sql, (start_date, end_date))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]} {row[2]}")
print()

sql="""
WITH DailyCrimeCounts AS (
    SELECT 
        reporting_district_rpt_dist_no AS rpt_dist_no,
        cr.crime_chronicle_date_occ AS crime_date,
        COUNT(*) AS daily_crimes
    FROM crime_report AS cr
    WHERE cr.crime_chronicle_date_occ BETWEEN %s AND %s
    GROUP BY cr.reporting_district_rpt_dist_no, cr.crime_chronicle_date_occ 
)

SELECT 
    rpt_dist_no, 
    crime_date,
    daily_crimes
FROM 
    DailyCrimeCounts
ORDER BY 
    daily_crimes DESC
LIMIT 5;
"""
cursor.execute(sql, (start_date, end_date))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]} {row[2]}")
print()

## --8 
#  ???


# -- 10
c = 113
sql = """
    -- Create a table with unique crime dates for each area
    WITH area_dates AS (
        SELECT area_name, cr.crime_chronicle_date_occ AS date
        FROM crime_report AS cr
        INNER JOIN area ON cr.area_area_id = area.area_id
        INNER JOIN crime_incident_crime_code AS code ON cr.dr_no = code.dr_no
        WHERE code.crm_cd = %s  -- Filter for the specific crime code
        GROUP BY area_name, cr.crime_chronicle_date_occ
    )

    -- Final query to find the longest time gap without the specific crime
    SELECT a1.area_name, 
        a1.date AS start_date,  -- Start of the gap period
        MIN(a2.date) AS end_date,  -- Earliest next date (end of the gap period)
        MIN(a2.date) - a1.date AS gap  -- Calculate the time gap
    FROM area_dates AS a1
    INNER JOIN area_dates AS a2 
        ON a1.area_name = a2.area_name  -- Join on the same area
        AND a1.date < a2.date  -- Ensure that a2.date is after a1.date
    GROUP BY a1.area_name, a1.date
    ORDER BY gap DESC  -- Sort by the longest gap in descending order
    LIMIT 1;  -- Return only the record with the longest gap
"""
cursor.execute(sql, (c,))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]} {row[1]} {row[2]}")
print()

c = 954
sql = """
    -- Create a table with unique crime dates for each reporting district
    WITH rpt_dist_dates AS (
        SELECT cr.reporting_district_rpt_dist_no AS rpt_dist_no, cr.crime_chronicle_date_occ AS date
        FROM crime_report AS cr
        INNER JOIN crime_incident_crime_code AS code ON cr.dr_no = code.dr_no
        WHERE code.crm_cd = %s  -- Filter for the specific crime code
        GROUP BY rpt_dist_no, date
    )

    -- Final query to find the longest time gap without the specific crime
    SELECT a1.rpt_dist_no, 
           a1.date AS start_date,  -- Start of the gap period
           MIN(a2.date) AS end_date,  -- Earliest next date (end of the gap period)
           MIN(a2.date) - a1.date AS gap  -- Calculate the time gap
    FROM rpt_dist_dates AS a1
    INNER JOIN rpt_dist_dates AS a2 
        ON a1.rpt_dist_no = a2.rpt_dist_no  -- Join on the same rpt_dist_no
        AND a1.date < a2.date  -- Ensure that a2.date is after a1.date
    GROUP BY a1.rpt_dist_no, a1.date
    ORDER BY gap DESC  -- Sort by the longest gap in descending order
    LIMIT 1;  -- Return only the record with the longest gap
"""

cursor.execute(sql, (c,))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]} {row[1]} {row[2]} {row[3]}")
print()


# -- 12
t='00:01:00'
sql="""
    WITH dr_date_weapon AS(
        SELECT dr_no, date_rptd, weapon_weapon_used_cd AS weapon_cd, area_area_id AS area_id
        FROM crime_report 
        JOIN crime_report_has_weapon ON dr_no = crime_report_dr_no
        WHERE crime_chronicle_time_occ = %s
        GROUP BY dr_no, date_rptd, weapon_weapon_used_cd, area_area_id
        ORDER BY date_rptd, area_area_id, weapon_weapon_used_cd
    )
    SELECT date_rptd, weapon_cd, COUNT(DISTINCT area_id) AS record_count
    FROM dr_date_weapon 
    GROUP BY date_rptd, weapon_cd
    ORDER BY date_rptd, weapon_cd;
"""

cursor.execute(sql, (t,))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]} {row[1]} {row[2]}")
print()

cursor.close()
conn.close()
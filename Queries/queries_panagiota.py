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

# ------------------------------------------------------------------------------------------
# -- 2:  Find the total number of reports per day for a specific “Crm Cd” and time range  --
# ------------------------------------------------------------------------------------------
t1='10:23:00'
t2='10:26:00'
c=623
sql = """
    SELECT report.date_rptd, COUNT(report.dr_no)
    FROM la_crimes.crime_report AS report
    WHERE report.crime_type_crm_cd = %s AND 
          report.crime_chronicle_time_occ BETWEEN %s AND %s 
    GROUP BY report.date_rptd
    ORDER BY report.date_rptd;
"""

# Execute the query with parameters
cursor.execute(sql, (c, t1, t2))

# Fetch results
results = cursor.fetchall()
for row in results:
   print(f"{row[0]} -> {row[1]}")
print(len(results))
print()


# ---------------------------------------------------------------------------------------------------
# -- 4:  Find the average number of crimes occurred per hour (24 hours) for a specific date range. --
# ---------------------------------------------------------------------------------------------------
start_date = '2023-01-01'
end_date =  '2023-01-05'
sql = """
    SELECT count(report.dr_no) / count(distinct report.crime_chronicle_date_occ) AS avg_number_of_crimes
    FROM la_crimes.crime_report AS report 
    WHERE report.crime_chronicle_date_occ BETWEEN %s AND %s 
"""

# Execute the query with parameters
cursor.execute(sql, (start_date, end_date))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]}")
print()


#-------------------------------------------------------------------------------------------------
# -- 6:??  Find the top-5 Area names with regards to total number of crimes reported per day for a
#        specific date range. The same for Rpt Dist No.
#-----------------------------------------------------------------------------------------------
start_date = '2020-01-14'
end_date =  '2020-01-15'

sql="""
    SELECT 
        area_name,
        COUNT(*) AS total_crimes
    FROM la_crimes.crime_report 
    INNER JOIN la_crimes.area ON area_area_id = area_id
    WHERE date_rptd BETWEEN %s AND %s
    GROUP BY area_name
    ORDER BY total_crimes DESC
    LIMIT 5;
"""
cursor.execute(sql, (start_date, end_date))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]} {row[1]}")
print()

sql="""
    SELECT reporting_district_rpt_dist_no AS rpt_dist_no,
           COUNT(*) AS total_crimes
    FROM la_crimes.crime_report 
    WHERE date_rptd BETWEEN %s AND %s
    GROUP BY reporting_district_rpt_dist_no
    ORDER BY total_crimes DESC
    LIMIT 5;
"""
cursor.execute(sql, (start_date, end_date))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]} {row[1]}")
print()


# --------------------------------------------------------------------------------------------
# -- 8: Find the second most common crime that has co-occurred with a particular crime for a  
#      specific date range. 
# --------------------------------------------------------------------------------------------
crime = 948
start_date = '2021-09-01'
end_date =  '2025-10-16'

sql="""
    SELECT report.crime_type_crm_cd AS snd_crime, COUNT(report.crime_type_crm_cd) as frequency
    FROM la_crimes.crime_report AS report
    WHERE report.crime_type_crm_cd <> %s AND 
          (report.crime_chronicle_date_occ, report.crime_chronicle_time_occ) IN  
                                  ( SELECT report.crime_chronicle_date_occ, report.crime_chronicle_time_occ
                                    FROM la_crimes.crime_report AS report
                                    WHERE report.crime_type_crm_cd = %s AND 
                                          report.crime_chronicle_date_occ BETWEEN %s AND %s )
    GROUP BY report.crime_type_crm_cd
    ORDER BY frequency DESC
    LIMIT 1 OFFSET 1;    
"""

cursor.execute(sql, (crime, crime, start_date, end_date))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]} {row[1]}")
print()

# --------------------------------------------------------------------------------------------
# -- 10: Find the area with the longest time range without an occurrence of a specific crime. 
#        Include the time range in the results. The same for Rpt Dist No.
# --------------------------------------------------------------------------------------------
c = 113
sql = """
    -- Create a table with unique crime dates for each area
    WITH area_dates AS (
        SELECT area_name, crime_chronicle_date_occ AS date
        FROM la_crimes.crime_report 
        INNER JOIN la_crimes.area ON area_area_id = area_id
        WHERE crime_type_crm_cd  = %s  
        GROUP BY area_name, date
    )

    -- Final query to find the longest time gap without the specific crime
    SELECT a1.area_name, 
        a1.date AS start_date,  -- Start of the gap period
        MIN(a2.date) AS end_date,  -- Earliest next date (end of the gap period)
        MIN(a2.date) - a1.date AS gap  -- Calculate the time gap
    FROM area_dates AS a1
    INNER JOIN area_dates AS a2 ON a1.area_name = a2.area_name AND a1.date < a2.date  -- Ensure that a2.date is after a1.date
    GROUP BY a1.area_name, a1.date
    ORDER BY gap DESC  
    LIMIT 1; 
"""
cursor.execute(sql, (c,))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]} {row[1]} {row[2]}")
print()

c = 954
sql="""
    WITH rpt_dist_dates AS (
        SELECT reporting_district_rpt_dist_no AS rpt_dist_no, crime_chronicle_date_occ AS date
        FROM la_crimes.crime_report 
        WHERE crime_type_crm_cd  = %s  
        GROUP BY rpt_dist_no, date
    )

    SELECT a1.rpt_dist_no, a1.date AS start_date,  MIN(a2.date) AS end_date, MIN(a2.date) - a1.date AS gap  
    FROM rpt_dist_dates AS a1
    INNER JOIN rpt_dist_dates AS a2 ON a1.rpt_dist_no = a2.rpt_dist_no AND a1.date < a2.date  
    GROUP BY a1.rpt_dist_no, a1.date
    ORDER BY gap DESC  
    LIMIT 1;
"""


cursor.execute(sql, (c,))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]} {row[1]} {row[2]} {row[3]}")
print()

# ------------------------------------------------------------------------------------------
# -- 12:  Find the number of division of records for crimes reported on the same day in  
#         different areas using the same weapon for a specific time range.
# ------------------------------------------------------------------------------------------

start_time='00:00:00'
end_time='23:59:00'
sql="""
    WITH dr_date_weapon AS(
        SELECT dr_no, date_rptd, weapon_weapon_used_cd AS weapon_cd, area_area_id AS area_id
        FROM la_crimes.crime_report 
        JOIN la_crimes.crime_report_has_weapon ON dr_no = crime_report_dr_no
        WHERE crime_chronicle_time_occ BETWEEN %s AND %s
        GROUP BY dr_no, date_rptd, weapon_weapon_used_cd, area_area_id
        ORDER BY date_rptd, weapon_weapon_used_cd, area_area_id
    ),
    RemoveDuplicates AS(
        SELECT date_rptd, weapon_cd, area_id
        FROM dr_date_weapon 
        GROUP BY date_rptd, weapon_cd, area_id
        HAVING COUNT(area_id) = 1
        ORDER BY date_rptd, weapon_cd, area_id
    )
    SELECT date_rptd, weapon_cd, COUNT(*)
    FROM RemoveDuplicates
    GROUP BY date_rptd, weapon_cd
"""

cursor.execute(sql, (start_time,end_time))

# Fetch results
results = cursor.fetchall()
for row in results:
    print(f"{row[0]} {row[1]} {row[2]}")
print()

cursor.close()
conn.close()
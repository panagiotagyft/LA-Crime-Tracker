import psycopg2
from psycopg2.extras import RealDictCursor  # To get results as dictionaries
def execute_query(connection, query, params=()):
    """Helper function to execute a query and return results."""
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

# Query 1: Reports Per Crime Code Within Time Range, time in millitary format (t1 <= x <= t2)
def get_reports_per_crime_code_in_time_range(connection, start_time, end_time):
    """
    Query to find the total number of reports per Crime Code within a time range. format is millitary time e.g. 0000-2359
    """
    query = """
        SELECT crm_cd, COUNT(*) AS report_count
        FROM Crime_Report
        JOIN Timestamp ON Crime_Report.timestamp_id = Timestamp.timestamp_id
        WHERE Timestamp.time_occ BETWEEN %s AND %s
        GROUP BY crm_cd
        ORDER BY report_count DESC;
    """
    results = execute_query(connection, query, (start_time, end_time))
    print("results lentgh: ", len(results))
    print("Query 1: Total number of reports per Crime Code:")
    total = 0
    for row in results:
        total += row[1]
        print(f"Crime Code: {row[0]}, Report Count: {row[1]}")
    print(f"Total reports: {total}")
    
    #CHANGE PRITNSSSSSS
    #MAYBE ADD A RETURN
    
# Query 3: Reports Per Area Name Within Time Range in format "YYYY-MM-DD"
def most_common_crime_per_area(connection, specific_date):
    """
    Query to find the most common crime per area on a specific date with format "YYYY-MM-DD".
    """
    query = f"""
    WITH FilteredCrimes AS (
        SELECT Area.area_id, Crime_report.crm_cd, crm_cd_2, crm_cd_3, crm_cd_4
        FROM Crime_report
        JOIN Reporting_district ON Crime_report.area_id = Reporting_district.area_id
        JOIN Area ON Reporting_district.area_id = Area.area_id
        JOIN Crime_code ON Crime_report.crm_cd = Crime_code.crm_cd_id
        WHERE date_rptd = %s AND Crime_code.crm_cd != -1 
    ),
    FlattenedCrimes AS (
        SELECT 
            area_id,
            FilteredCrimes.crm_cd AS crime_code
        FROM FilteredCrimes
        UNION ALL
        SELECT 
            area_id,
            FilteredCrimes.crm_cd_2 AS crime_code
        FROM FilteredCrimes
        UNION ALL
        SELECT 
            area_id,
            FilteredCrimes.crm_cd_3 AS crime_code
        FROM FilteredCrimes
        UNION ALL
        SELECT 
            area_id,
            crm_cd_4 AS crime_code
        FROM FilteredCrimes
    ),
    CrimeCounts AS (
        SELECT 
            area_id,
            crime_code,
            COUNT(*) AS crime_count
        FROM FlattenedCrimes
        GROUP BY area_id, crime_code
    ),
    MostCommonCrimes AS (
        SELECT 
            area_id,
            crime_code,
            crime_count,
            RANK() OVER (PARTITION BY area_id ORDER BY crime_count DESC) AS rank
        FROM CrimeCounts
    )
    SELECT 
        ---area_name,
        MostCommonCrimes.area_id,
        crime_code,
        Crime_code.crm_cd_desc,
        crime_count
    FROM MostCommonCrimes, Crime_code
   WHERE Crime_code.crm_cd = MostCommonCrimes.crime_code AND crime_code = MostCommonCrimes.crime_code ;
"""

    print("Date is ", specific_date)   
    specific_date = '2022-11-20' 
    cursor = connection.cursor()  # Use RealDictCursor for dict-like rows
    cursor.execute(query, (specific_date,))
    reports = cursor.fetchall()
    
    
    print("Query 3: Most common crime code within bounding box on the specific date:")
    for row in reports:
        print(f"Crime Code: {row[0]}, Code: {row[1]}, Frequency: {row[2]}")
        

    
    # print("Most Common Crime per Area on Specific Date:")
    # for report in reports:
    #     print("Area id : {report[0]}, Crime Code: {report[1]}, Count: {report[2]}")
    
    # verify_query = """
    # SELECT area_id, crm_cd, crm_cd_2, crm_cd_3, crm_cd_4
    # FROM Crime_Report
    # WHERE date_rptd = %s
    # """
    
    # cursor.execute(verify_query, (specific_date,))
    # area_reports = cursor.fetchall()
    
    # report = execute_query(connection, query, (specific_date,))
    # print("Area Reports (area_id, crm_cd, crm_cd_2, crm_cd_3, crm_cd_4):")
    # for row in area_reports:
    #     print("Area id: {row[0]}, Crime Codes: {row[1]}, {row[2]}, {row[3]}, {row[4]}")
    

    
    
    
    # results = execute_query(connection, query)
    # print("Query 2: Most common crime per area on the specific date:")
    # #IDIOTIC WAY TO PRINT ONLY THE FIRST ROW
    # for row in results:
    #     print(f"Area: {row[0]}\t, Crime Code: \t{row[1]}\t, Frequency: {row[2]}")
    #     break

# Query 5 - Most Common Crime Code Within Bounding Box on Specific Date
def most_common_crime_cd_bounding_box(connection, specific_date, min_lat, max_lat, min_lon, max_lon):
    """
    Query to find the most common crime code within a bounding box on a specific date.
    Date should be in the format "YYYY-MM-DD".
    """
    query = f"""
    SELECT crm_cd, frequency FROM (
        SELECT 
            ct.crm_cd,
            COUNT(*) AS frequency,
            RANK() OVER (ORDER BY COUNT(*) DESC) AS rank
        FROM crime_report cr
        JOIN crime_incident_crime_code cicc ON cr.dr_no = cicc.dr_no
        JOIN Crime_code ct ON cicc.crm_cd = ct.crm_cd
        JOIN crime_location cl ON cr.crime_location_location = cl.location
        WHERE cr.crime_chronicle_date_occ = '{specific_date}' 
          AND cl.lat BETWEEN {min_lat} AND {max_lat}     
          AND cl.lon BETWEEN {min_lon} AND {max_lon}     
        GROUP BY ct.crm_cd
    ) AS ranked_crimes
    WHERE rank = 1;
    """
    results = execute_query(connection, query)
    print("Query 3: Most common crime code within bounding box on the specific date:")
    for row in results:
        print(f"Crime Code: {row[0]}, Frequency: {row[1]}")
        


def get_earliest_and_latest_dates(connection):
    query = """
    SELECT MIN(crime_chronicle_date_occ) AS earliest_date,
           MAX(crime_chronicle_date_occ) AS latest_date
    FROM crime_report;
    """
    
    results = execute_query(connection, query)
    for row in results:
        print(f"Earliest Date: {row[0]}, Latest Date: {row[1]}")
        

    
        
# Query 7 -problems with the query
def most_common_cooccurring_crimes_in_top_area(connection, start_date, end_date):    
    
    top_area_query = """
    SELECT a.area_id, a.area_name
    FROM crime_report cr
    JOIN area a ON cr.area_area_id = a.area_id
    WHERE cr.crime_chronicle_date_occ BETWEEN %s AND %s
    GROUP BY a.area_id, a.area_name
    ORDER BY COUNT(*) DESC
    LIMIT 1;
    """
    
    cooccurring_crimes_query = """
    WITH AreaIncidentCounts AS (
        SELECT area_area_id
        FROM crime_report
        WHERE crime_chronicle_date_occ BETWEEN %s AND %s
        GROUP BY area_area_id
        ORDER BY COUNT(*) DESC
        LIMIT 1
    )
    SELECT 
        cic1.crm_cd AS crime1,
        cic2.crm_cd AS crime2,
        COUNT(*) AS co_occurrence_count
    FROM crime_report cr
    JOIN crime_incident_crime_code cic1 ON cr.dr_no = cic1.dr_no
    JOIN crime_incident_crime_code cic2 ON cr.dr_no = cic2.dr_no 
        AND cic1.crm_cd < cic2.crm_cd
    WHERE cr.area_area_id = (SELECT area_area_id FROM AreaIncidentCounts)
      AND cr.crime_chronicle_date_occ BETWEEN %s AND %s
    GROUP BY crime1, crime2
    ORDER BY co_occurrence_count DESC;
    """
    
    
    # Execute the query to find the area with the most incidents
    results = execute_query(connection, top_area_query, (start_date, end_date))
    
    for row in results:
        print(f"Top Area ID: {row[0]}")
    
    # Get the area ID of the top area
    top_area_id = results[0]
    print(f"Top Area ID: {top_area_id}")
    
    # Execute the main co-occurrence query
    results = execute_query(connection, cooccurring_crimes_query, (start_date, end_date, start_date, end_date))    
    # Print each crime pair and their co-occurrence count
    if results:
        print("Co-occurring Crime Pairs in the Area with the Most Incidents:")
        for row in results:
            print(f"Crime Pair: {row[0]} and {row[1]}, Co-occurrence Count: {row[2]}")
    else:
        print("No co-occurring crimes found in the specified area and date range.")
    
    
    
    
    # query = """
    # WITH AreaIncidentCounts AS (
    #     SELECT 
    #         cr.area_area_id,
    #         COUNT(*) AS incident_count
    #     FROM crime_report cr
    #     WHERE cr.crime_chronicle_date_occ BETWEEN %s AND %s
    #     GROUP BY cr.area_area_id
    #     ORDER BY incident_count DESC
    #     LIMIT 1
    # ), CoOccurredCrimes AS (
    #     SELECT 
    #         cic1.crm_cd AS crime1,
    #         cic2.crm_cd AS crime2,
    #         COUNT(*) AS co_occurrence_count
    #     FROM crime_report cr
    #     JOIN crime_incident_crime_code cic1 ON cr.dr_no = cic1.dr_no
    #     JOIN crime_incident_crime_code cic2 ON cr.dr_no = cic2.dr_no 
    #         AND cic1.crm_cd < cic2.crm_cd
    #     WHERE cr.area_area_id = (SELECT area_area_id FROM AreaIncidentCounts)
    #       AND cr.crime_chronicle_date_occ BETWEEN %s AND %s
    #     GROUP BY crime1, crime2
    #     ORDER BY co_occurrence_count DESC
    # )
    # SELECT crime1, crime2, co_occurrence_count
    # FROM CoOccurredCrimes;
    # """
   
    
    # results = execute_query(connection, query, (start_date, end_date, start_date, end_date))
    
    # print("Query 7: Most common co-occurring crimes in the top area:")
    # for row in results:
    #     print(f"Crime 1: {row[0]}, Crime 2: {row[1]}, Co-occurrence Count: {row[2]}")
        
        
    



#Query 9 - Most Common Weapon Used by Age Group, questinoble results
def most_common_weapon_to_age_group(connection):
    query = """
    SELECT age_group, weapon_desc, frequency
    FROM (
        SELECT 
            FLOOR(v.vict_age / 5) * 5 AS age_group,
            w.weapon_desc,
            COUNT(*) AS frequency,
            RANK() OVER (PARTITION BY FLOOR(v.vict_age / 5) * 5 ORDER BY COUNT(*) DESC) AS rank
        FROM victim v
        JOIN crime_report_has_weapon crw ON v.dr_no = crw.crime_report_dr_no
        JOIN weapon w ON crw.weapon_weapon_used_cd = w.weapon_used_cd
        WHERE v.vict_age IS NOT NULL
        GROUP BY age_group, w.weapon_desc
    ) AS ranked_weapons
    WHERE rank = 1
    ORDER BY age_group;

    """
    
    results = execute_query(connection, query)
    print("Query 9: Most common weapon used by age group:")
    for row in results:
        print(f"Age Group: {row[0]}, Weapon: {row[1]}, Frequency: {row[2]}")
        
        

def all_weapons_by_age_group_desc(connection):
    query = """
    SELECT 
        FLOOR(v.vict_age / 5) * 5 AS age_group,
        w.weapon_desc,
        COUNT(*) AS frequency
    FROM victim v
    JOIN crime_report_has_weapon crw ON v.dr_no = crw.crime_report_dr_no
    JOIN weapon w ON crw.weapon_weapon_used_cd = w.weapon_used_cd
    WHERE v.vict_age IS NOT NULL
    GROUP BY age_group, w.weapon_desc
    ORDER BY age_group, frequency DESC;
    """
    
    results = execute_query(connection, query)
    for row in results:
        print(f"Age Group: {row[0]}, Weapon: {row[1]}, Frequency: {row[2]}")
        
#Query 11 - Areas with Multiple Reports on Two Crimes
def areas_with_multiple_reports_on_two_crimes(connection, crime1, crime2):
    """
    Query to find areas with multiple reports on two crimes.
    Select from existing crime types.
    """
    query = f"""
    SELECT area_name, report_date
    FROM (
        SELECT 
            a.area_name,
            cr.crime_chronicle_date_occ AS report_date,
            ct.crm_cd_desc AS Crime_code,
            COUNT(*) AS report_count
        FROM crime_report cr
        JOIN crime_incident_crime_code cicc ON cr.dr_no = cicc.dr_no
        JOIN Crime_code ct ON cicc.crm_cd = ct.crm_cd
        JOIN area a ON cr.area_area_id = a.area_id
        WHERE ct.crm_cd_desc IN ('{crime1}', '{crime2}')
        GROUP BY a.area_name, cr.crime_chronicle_date_occ, ct.crm_cd_desc
    ) AS crime_counts
    GROUP BY area_name, report_date
    HAVING COUNT(DISTINCT Crime_code) = 2 
       AND MIN(report_count) > 1
    ORDER BY area_name, report_date;
    """
    
    results = execute_query(connection, query)
    print("Query 5: Areas with multiple reports on two crimes:")    #copilot prints moment
    for row in results:
        print(f"Area: {row[0]}, Report Date: {row[1]}")
        

def list_all_Crime_codes_by_frequency(connection):
    query = """
    SELECT crm_cd_desc, COUNT(*) AS frequency
    FROM crime_incident_crime_code cicc
    JOIN Crime_code ct ON cicc.crm_cd = ct.crm_cd
    GROUP BY crm_cd_desc
    ORDER BY frequency DESC;
    """
    
    results = execute_query(connection, query)
    print("Query 6: List of all crime types:")
    for row in results:
        print(f"Crime Type: {row[0]}, Frequency: {row[1]}")
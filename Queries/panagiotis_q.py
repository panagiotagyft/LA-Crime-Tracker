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
        SELECT Crime_code.crm_cd, COUNT(*) AS report_count
        FROM Crime_Report
        JOIN Timestamp ON Crime_Report.timestamp_id = Timestamp.timestamp_id
        JOIN Crime_code ON Crime_Report.crm_cd = Crime_code.crm_cd_id
        WHERE Timestamp.time_occ BETWEEN %s AND %s
        GROUP BY Crime_code.crm_cd
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
        JOIN Area ON Crime_report.area_id = Area.area_id
        WHERE date_rptd = %s
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
        crime_count
    FROM MostCommonCrimes
    JOIN Crime_code ON MostCommonCrimes.crime_code = Crime_code.crm_cd_id
    WHERE Crime_code.crm_cd != -1
"""

    print("Date is ", specific_date)   
    cursor = connection.cursor()  # Use RealDictCursor for dict-like rows
    cursor.execute(query, (specific_date,))
    reports = cursor.fetchall()
    
    
    print("Query 3: Most common crime code with specific date:")
    for row in reports:
        print(f"Area Code: {row[0]}, Crime Code: {row[1]}, Frequency: {row[2]}")
        

    
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
    
    # print("Area Reports (area_id, crm_cd, crm_cd_2, crm_cd_3, crm_cd_4):")
    # print(area_reports)    

    
    
    
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
    SELECT crm_cd, COUNT(*) AS frequency
    FROM crime_report cr
    JOIN crime_location cl ON cr.location_id = cl.location_id
    JOIN Timestamp ts ON cr.timestamp_id = ts.timestamp_id
    WHERE ts.date_occ = '{specific_date}'::date
    AND cl.lat >= {min_lat} AND cl.lat <= {max_lat}     
    AND cl.lon >= {min_lon} AND cl.lon <= {max_lon}     
    GROUP BY cr.crm_cd
    ORDER BY frequency DESC
    LIMIT 5;
    """

    results = execute_query(connection, query)
    print("Query 5: Most common crime code within bounding box on the specific date:  ", specific_date)
    for row in results:
        print(f"Crime Code: {row[0]}, Frequency: {row[1]}")
    return results    
        
# Query 7 -problems with the query
def most_common_cooccurring_crimes_in_top_area(connection, start_date, end_date):    
    
    top_area_query = """
    SELECT a.area_id, a.area_name
    FROM crime_report cr
    JOIN area a ON cr.area_id = a.area_id
    JOIN Timestamp ts ON cr.timestamp_id = ts.timestamp_id
    WHERE date_occ BETWEEN %s AND %s
    GROUP BY a.area_id, a.area_name
    ORDER BY COUNT(*) DESC
    LIMIT 1;
    """
    #! add crimes of that time as table
    cooccurring_crimes_query = """
    WITH AreaIncidentCounts AS (
        SELECT area_id
        FROM crime_report
        JOIN Timestamp ON crime_report.timestamp_id = Timestamp.timestamp_id
        WHERE date_occ BETWEEN %s AND %s
        GROUP BY area_id
        ORDER BY COUNT(*) DESC
        LIMIT 1
    )
    SELECT 
        cc1.crm_cd AS crime1,
        cc2.crm_cd AS crime2,
        COUNT(*) AS co_occurrence_count
    FROM crime_report cr1
    JOIN crime_report cr2 
        ON cr1.area_id = cr2.area_id 
        AND cr1.timestamp_id = cr2.timestamp_id
        AND cr1.dr_no < cr2.dr_no
    JOIN Crime_code cc1 ON cc1.crm_cd_id = cr1.crm_cd
    JOIN Crime_code cc2 ON cc2.crm_cd_id = cr2.crm_cd AND cc1.crm_cd_id < cc2.crm_cd_id
    JOIN Timestamp ts ON cr1.timestamp_id = ts.timestamp_id
    WHERE cr1.area_id = (SELECT area_id FROM AreaIncidentCounts)
    AND ts.date_occ BETWEEN %s AND %s
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
    results = execute_query(connection, cooccurring_crimes_query, (start_date, end_date, start_date, end_date,))    
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
        
        
    



#Query 9 - Most Common Weapon Used by Age Group, questionable results
def most_common_weapon_to_age_group(connection):
    query = """
    SELECT age_group, weapon_cd, weapon_desc, frequency
    FROM (
        SELECT 
            FLOOR(v.vict_age / 5) * 5 AS age_group,
            w.weapon_cd,
            w.weapon_desc,
            COUNT(*) AS frequency,
            RANK() OVER (PARTITION BY FLOOR(v.vict_age / 5) * 5 ORDER BY COUNT(*) DESC) AS rank
        FROM victim v
        JOIN Crime_report cr ON v.dr_no = cr.dr_no
        JOIN Weapon w ON cr.weapon_cd = w.weapon_cd
        WHERE v.vict_age IS NOT NULL AND v.vict_age > 0
            AND w.weapon_cd > 0                             --- to avoid the -1 weapon code, non existent weapon
        GROUP BY age_group, w.weapon_cd, w.weapon_desc
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
            ts.date_occ AS report_date,
            cc.crm_cd_desc,
            COUNT(*) AS report_count
        FROM crime_report cr
        JOIN Crime_code cc ON cc.crm_cd_id = cr.crm_cd
        JOIN area a ON cr.area_id = a.area_id
        JOIN Timestamp ts ON cr.timestamp_id = ts.timestamp_id
        WHERE cc.crm_cd_desc IN ('{crime1}', '{crime2}')
        GROUP BY a.area_name, ts.date_occ, cc.crm_cd_desc
    ) AS crime_counts
    GROUP BY area_name, report_date
    HAVING COUNT(DISTINCT crm_cd_desc) = 2
    AND MIN(report_count) > 1  -- Ensure at least 2 reports for each crime
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
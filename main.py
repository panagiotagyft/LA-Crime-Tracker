import time
import psycopg2
import random
from psycopg2 import OperationalError, sql
from Queries.panagiotis_q import *




def execute_query(connection, query, values=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

if __name__ == "__main__":
    
    # Replace with your actual details
    DB_HOST = 'localhost'
    # DB_HOST = '0.0.0.0'
    DB_NAME = 'LA_Crimes'
    DB_USER = 'postgres'
    DB_PASS = 'example'
    DB_PORT = '5432'
    CSV_FILE_PATH = 'Crime_Data_from_2020_to_Present_20241112.csv'
    sql_file_path = 'create_tables.sql' # Good practice to keep SQL queries in a separate file

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()

    if conn:
        # Create table if it doesn't exist
        start_time = "00:00:00"
        end_time = "24:00:00"
        # get_reports_per_crime_code_in_time_range(conn, str(start_time), str(end_time))

                    
        # Example usage with a single date in the format "YYYY-MM-DD"
        specific_date = '2024-01-01'  # Specific date to query
        most_common_crime_per_area(conn, specific_date)
        
        
        # #MUST PREPROCESS MESSY DATA!!!
        # # Example usage
        # specific_date = '2024-10-28'  # Date for the query
        # min_lat = 34242             # Replace with minimum latitude of bounding box
        # max_lat = 337823             # Replace with maximum latitude of bounding box
        # min_lon = -1170000           # Replace with minimum longitude of bounding box
        # max_lon = -118243           # Replace with maximum longitude of bounding box

        # result = most_common_crime_cd_bounding_box(conn, specific_date, min_lat, max_lat, min_lon, max_lon)
        # if result:
        #     for row in result:
        #         print(f"Crime Code: {row[0]}, Frequency: {row[1]}")
        
        # conn.close()
        # most_common_weapon_to_age_group(conn)
        # all_weapons_by_age_group_desc(conn)   #usefull to cinfirm the results of the previous query
        # list_all_crime_types_by_frequency(conn)
        # areas_with_multiple_reports_on_two_crimes(conn, 'VEHICLE - STOLEN', 'BATTERY - SIMPLE ASSAULT')
        # get_earliest_and_latest_dates(conn)
        # most_common_cooccurring_crimes_in_top_area(conn, '2020-01-01', '2024-10-29')
        
        
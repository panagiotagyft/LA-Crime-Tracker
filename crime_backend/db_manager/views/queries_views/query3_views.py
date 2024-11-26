from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

class Query3View(APIView):
    def get(self, request):

        def parse_date(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        date = parse_date(request.query_params.get('date'))

        if not date:
            return Response({"Error": "Date is required!!"}, status=400)
  
        print(date)
        try:
            with connection.cursor() as cursor:

                sql="""
                    WITH FlattenedCrimes AS (
                        SELECT area_id, code.crm_cd AS crime_code
                        FROM Crime_report AS report
                        JOIN Crime_code AS code ON code.crm_cd_id = report.crm_cd
                        JOIN Timestamp AS date ON date.timestamp_id = report.timestamp_id
                        WHERE code.crm_cd != -1 AND date.date_occ = %s

                        UNION ALL

                        SELECT area_id, code.crm_cd AS crime_code
                        FROM Crime_report AS report
                        JOIN Crime_code AS code ON code.crm_cd_id = report.crm_cd_2
                        JOIN Timestamp AS date ON date.timestamp_id = report.timestamp_id
                        WHERE code.crm_cd != -1 AND date.date_occ = %s

                        UNION ALL

                        SELECT area_id, code.crm_cd AS crime_code
                        FROM Crime_report AS report
                        JOIN Crime_code AS code ON code.crm_cd_id = report.crm_cd_3
                        JOIN Timestamp AS date ON date.timestamp_id = report.timestamp_id
                        WHERE code.crm_cd != -1 AND date.date_occ = %s

                        UNION ALL

                        SELECT area_id, code.crm_cd AS crime_code
                        FROM Crime_report AS report
                        JOIN Crime_code AS code ON code.crm_cd_id = report.crm_cd_4
                        JOIN Timestamp AS date ON date.timestamp_id = report.timestamp_id
                        WHERE code.crm_cd != -1 AND date.date_occ = %s
                    ),
                    -- Step 2: Calculate the crime counts for each area and crime code
                    CrimeCounts AS (
                        SELECT 
                            area_id,
                            crime_code,
                            COUNT(*) AS crime_count
                        FROM FlattenedCrimes
                        GROUP BY area_id, crime_code
                        -- Group by area and crime code to get the number of occurrences
                    )
                    -- Step 3: Use DISTINCT ON to select the most common crime per area
                    SELECT DISTINCT ON (area_id)
                        area_id,
                        crime_code,
                        crime_count
                    FROM CrimeCounts
                    ORDER BY area_id, crime_count DESC;


                """
                cursor.execute(sql, [date, date, date, date])
                rows = cursor.fetchall()
                
            if not rows:  # Check if the list is empty.
                return Response({"message": "No data available for the given time range."}, status=200)
            
            print(len(rows))
            # Formatting results in JSON.
            results = [{"Area Code": row[0], "The most frequent crime": row[1]} for row in rows]
            print(results)
            return Response(results, status=200)
        
        except Exception as e:
                return Response({"error": str(e)}, status=500)
        
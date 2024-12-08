from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

class Query11View(APIView):
    def get(self, request):
        
        crime_code1 = request.query_params.get('crime_code1')
        crime_code2 = request.query_params.get('crime_code2')
    
        sql = """
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

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, [crime_code1, crime_code2])
                rows = cursor.fetchall()
                
            if not rows:  # Check if the list is empty.
                return Response({"message": "No data available for the given time range."}, status=200)
            
            # Formatting results in JSON.
            results = [{"Area": row[0]} for row in rows]
            return Response(results, status=200)
        
        except Exception as e:
                return Response({"error": str(e)}, status=500)
        


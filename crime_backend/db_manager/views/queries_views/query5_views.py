from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

class Query5View(APIView):
    def get(self, request):
        
        def parse_date(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        date = parse_date(request.query_params.get('date'))
        min_lat = float(request.query_params.get('min_lat'))
        max_lat = float(request.query_params.get('max_lat'))
        min_lon = float(request.query_params.get('min_lon'))
        max_lon = float(request.query_params.get('max_lon'))

        
        if not date or not min_lat or not max_lat or not min_lon or not max_lon:
            return Response({"Error": "Both date and bounding box GPS coordinates are required."}, status=400)

        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT cc.crm_cd, COUNT(*) AS frequency
                    FROM crime_report cr
                    JOIN crime_location cl ON cr.location_id = cl.location_id
                    JOIN Crime_code cc ON cr.crm_cd = cc.crm_cd_id
                    JOIN Timestamp ts ON cr.timestamp_id = ts.timestamp_id
                    WHERE ts.date_occ = '{specific_date}'
                    --AND cl.lat >= {min_lat} AND cl.lat <= {max_lat}     
                    --AND cl.lon >= {min_lon} AND cl.lon <= {max_lon}     
                    GROUP BY cc.crm_cd
                    ORDER BY frequency DESC
                    LIMIT 5;
                """
                cursor.execute(sql, [date, min_lat, max_lat, min_lon, max_lon])
                rows = cursor.fetchall()
                    
            if not rows:
                return Response([], status=200)

            result = [{"crime_code": row[0], "crime_count": row[1]} for row in rows]
            return Response(result, status=200)
                
        except Exception as e:
            return Response({"error": str(e)}, status=500)

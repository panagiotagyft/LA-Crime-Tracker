from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

class Query7View(APIView):
    def get(self, request):
        
        def parse_date(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        start_date = parse_date(request.query_params.get('startDate'))
        end_date = parse_date(request.query_params.get('endDate'))
        
        if not start_date or not end_date:
            return Response({"Error": "Start/End date are required!"}, status=400)

        try:
            with connection.cursor() as cursor:
                sql = """
                   #...
                """
                cursor.execute(sql, [start_date, end_date])
                rows = cursor.fetchall()
            
            if not rows:  # Check if the list is empty.
                return Response({"message": "No data available for the given time range."}, status=200)
            
            # Formatting results in JSON.
            results = [{"Area name": row[0], "Crime 1": row[1], "Crime 2": row[2], "Pair Count": row[3]} for row in rows]
            return Response(results, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)

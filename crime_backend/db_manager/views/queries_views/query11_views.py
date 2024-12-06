from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

class Query11View(APIView):
    def get(self, request):
        
        crime_code1 = request.query_params.get('crime_code1')
        crime_code2 = request.query_params.get('crime_code2')
    
        sql = """
        ....
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
        


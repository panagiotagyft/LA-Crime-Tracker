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
                --- revert
                   #....
                """
                cursor.execute(sql, [date, date, date, date])
                rows = cursor.fetchall()
                
            if not rows:  # Check if the list is empty.
                return Response({"message": "No data available for the given time range."}, status=200)
            
            # Formatting results in JSON.
            results = [{"Area Code": row[0], "The most frequent crime": row[1]} for row in rows]
            return Response(results, status=200)
        
        except Exception as e:
                return Response({"error": str(e)}, status=500)
        

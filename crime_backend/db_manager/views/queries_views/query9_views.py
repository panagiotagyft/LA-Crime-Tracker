from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response

class Query9View(APIView):
    def get(self, request):

        try:
            print("Hello")
            with connection.cursor() as cursor:

                sql="""
                    # ...
                """
                cursor.execute(sql)
                rows = cursor.fetchall()
                
            if not rows:  # Check if the list is empty.
                return Response({"message": "No data available for the given time range."}, status=200)
            
            # Formatting results in JSON.
            results = [{"Age Group": row[0], "Most common weapon": row[1], "Occurrence Count": row[2]} for row in rows]
            return Response(results, status=200)
        
        except Exception as e:
                return Response({"error": str(e)}, status=500)
        


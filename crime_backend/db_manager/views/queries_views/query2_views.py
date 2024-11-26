from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response

class Query2View(APIView):
    def get(self, request):
        start_time = request.query_params.get('startTime')
        end_time = request.query_params.get('endTime')
        crime_code = request.query_params.get('crmCd')

        if not start_time or not end_time or not crime_code:
            return Response({"Error": "Start/End time and crime code are required!!"}, status=400)


        try:
            with connection.cursor() as cursor:

                sql="""
                    SELECT report.date_rptd, COUNT(report.dr_no) as total_reports
                    FROM Crime_Report AS report
                    JOIN Timestamp AS time ON report.timestamp_id = time.timestamp_id
                    WHERE report.crm_cd = %s AND time.time_occ BETWEEN %s AND %s 
                    GROUP BY report.date_rptd
                    ORDER BY total_reports DESC;
                """
                cursor.execute(sql, [crime_code, start_time, end_time])
                rows = cursor.fetchall()
                
            if not rows:  # Έλεγχος αν η λίστα είναι κενή
                return Response({"message": "No data available for the given time range."}, status=200)
            
            # Διαμόρφωση αποτελεσμάτων σε JSON
            results = [{"Reported Day": row[0], "Total number of reports": row[1]} for row in rows]
            return Response(results, status=200)
        
        except Exception as e:
                return Response({"error": str(e)}, status=500)
        


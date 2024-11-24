from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Query1View(APIView):
    def get(self, request):
        start_time = request.query_params.get('startTime')
        end_time = request.query_params.get('endTime')
        
        if not start_time or not end_time:
            return Response({"error": "Start time and end time are required."}, status=400)

        sql = """
            SELECT cd.crm_cd, COUNT(*) AS report_count
            FROM Crime_report AS rpt
            JOIN Crime_code AS cd ON rpt.crm_cd = cd.crm_cd_id
            JOIN Timestamp AS ts ON rpt.timestamp_id = ts.timestamp_id
            WHERE ts.time_occ BETWEEN %s AND %s
            GROUP BY cd.crm_cd
            ORDER BY report_count DESC;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, [start_time, end_time])
                rows = cursor.fetchall()

            # Διαμόρφωση αποτελεσμάτων σε JSON
            results = [{"crm_cd": row[0], "report_count": row[1]} for row in rows]
            print(len(rows))
            return Response(results, status=200)
        
        except Exception as e:
                return Response({"error": str(e)}, status=500)
        

class DropdownOptionsView(APIView):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                
                cursor.execute("SELECT area_id FROM Area")
                area_codes = [row[0] for row in cursor.fetchall()]
                area_codes = sorted(area_codes)

                # Παράδειγμα query για Crime Codes
                cursor.execute("""SELECT crm_cd 
                               FROM Crime_code
                               WHERE crm_cd != -1 """)
                crime_codes = [row[0] for row in cursor.fetchall()]
                crime_codes = sorted(crime_codes)

                cursor.execute("""SELECT premis_cd 
                               FROM Premises
                               WHERE premis_cd != -1""")
                premises = [row[0] for row in cursor.fetchall()]
                premises = sorted(premises)

                cursor.execute("""SELECT weapon_cd 
                               FROM Weapon
                               WHERE weapon_cd != -1""")
                weapons = [row[0] for row in cursor.fetchall()]
                weapons = sorted(weapons)

                cursor.execute("SELECT status_code FROM Status")
                statuses = [row[0] for row in cursor.fetchall()]
                statuses = sorted(statuses)

            data = {
                "area_codes": area_codes,
                "crime_codes": crime_codes,
                "premises": premises,
                "weapons": weapons,
                "statuses": statuses,
            }
           
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCodeDescriptionView(APIView):
    def get(self, request):
        table_name = request.query_params.get('type', None)
        code_value = request.query_params.get('code', None)
        print(table_name)
        print(code_value)
        if not table_name or not code_value:
            return Response({"error": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
              
                if table_name == "Area": query = f"SELECT area_name FROM Area WHERE area_id = %s"
                if table_name == "Crime_code": query = f"SELECT crm_cd_desc FROM Crime_code WHERE crm_cd = %s"
                if table_name == "Premises": query = f"SELECT premis_desc FROM Premises WHERE premis_cd = %s"
                if table_name == "Weapon": query = f"SELECT weapon_desc FROM Weapon WHERE weapon_cd = %s"
                if table_name == "Status": query = f"SELECT status_desc FROM Status WHERE status_code = %s"

                cursor.execute(query, [code_value])
                row = cursor.fetchone()

            print(row)
            if row:
                return Response({"description": row[0]}, status=status.HTTP_200_OK)
            return Response({"description": None}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from datetime import datetime

class GenerateDRNOView(APIView):
    def get(self, request):
        area_id = request.query_params.get('area_id', None)
        date_rptd = request.query_params.get('date_rptd', None)
        
        if not area_id or not date_rptd:
            return Response({"error": "Area ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            year2digit = date_rptd.year
            print(year2digit)
            print(area_id)
            with connection.cursor() as cursor:
                # Βρίσκουμε τον επόμενο διαθέσιμο αριθμό για το συγκεκριμένο Area ID και date_rptd
                query = """
                    SELECT COUNT(*) + 1 
                    FROM Crime_report 
                    WHERE area_id = %s AND YEAR(date_rptd) = %s;
                """
                cursor.execute(query, [area_id, year2digit])
                next_record_number = cursor.fetchone()[0]

            # Δημιουργούμε το DR_NO
            dr_no = f"{year2digit:02}{int(area_id):02}{next_record_number:05}"
            return Response({"dr_no": dr_no}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SaveNewCodeView(APIView):
    def post(self, request):
        code_type = request.data.get('type', None)
        code_value = request.data.get('code', None)
        description = request.data.get('description', None)

        if not code_type or not code_value or not description:
            return Response({"error": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)

        table_mapping = {
            "area_id": "Area",
            "crm_cd": "Crime_code",
            "premis_cd": "Premises",
            "weapon_used_cd": "Weapon",
            "status": "Status",
        }

        if code_type not in table_mapping:
            return Response({"error": "Invalid code type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                table_name = table_mapping[code_type]
                # Εισαγωγή νέου κωδικού
                query = f"INSERT INTO {table_name} (code, description) VALUES (%s, %s)"
                cursor.execute(query, [code_value, description])

            return Response({"message": "Code saved successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


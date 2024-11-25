from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

class DropdownOptionsView(APIView):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                
                cursor.execute("SELECT area_id FROM Area")
                area_codes = [row[0] for row in cursor.fetchall()]
                area_codes = sorted(area_codes)

                # Παράδειγμα query για Crime Codes
                cursor.execute("""SELECT crm_cd FROM Crime_code""")
                crime_codes = [row[0] for row in cursor.fetchall()]
                crime_codes = sorted(crime_codes)

                cursor.execute("""SELECT premis_cd FROM Premises""")
                premises = [row[0] for row in cursor.fetchall()]
                premises = sorted(premises)

                cursor.execute("""SELECT weapon_cd FROM Weapon""")
                weapons = [row[0] for row in cursor.fetchall()]
                weapons = sorted(weapons)

                cursor.execute("SELECT status_code FROM Status")
                statuses = [row[0] for row in cursor.fetchall()]
                statuses = sorted(statuses)

                cursor.execute("SELECT rpt_dist_no FROM Crime_report")
                rpt_dists = [row[0] for row in cursor.fetchall()]
                rpt_dists = sorted(list(set(rpt_dists)))

                cursor.execute("SELECT vict_sex FROM Victim")
                victims_sex = [row[0] for row in cursor.fetchall()]
                victims_sex = sorted(dict.fromkeys(victims_sex))

                cursor.execute("SELECT vict_descent FROM Victim")
                victims_descent = [row[0] for row in cursor.fetchall()]
                victims_descent = sorted(dict.fromkeys(victims_descent))

                cursor.execute("SELECT mocodes FROM Crime_report")
                mocodes = [row[0] for row in cursor.fetchall()]
                mocodes = list(dict.fromkeys(mocodes))

            data = {
                "area_codes": area_codes,
                "crime_codes": crime_codes,
                "premises": premises,
                "weapons": weapons,
                "statuses": statuses,
                "rpt_dists": rpt_dists,
                "victims_sex": victims_sex,
                "victims_descent": victims_descent,
                "mocodes": mocodes,
            }
           
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCodeDescriptionView(APIView):
    def get(self, request):
        table_name = request.query_params.get('type', None)
        code_value = request.query_params.get('code', None)
        # print(table_name)
        # print(code_value)
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

            # print(row)
            if row:
                return Response({"description": row[0]}, status=status.HTTP_200_OK)
            return Response({"description": None}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerateDRNOView(APIView):
    def get(self, request):
        area_id = request.query_params.get('area_id', None)
        date_rptd = request.query_params.get('date_rptd', None)
        print(f"Received area_id: {area_id}, date_rptd: {date_rptd}")

        if not area_id or not date_rptd:
            return Response({"error": "Area ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date_rptd = datetime.strptime(date_rptd, "%Y-%m-%d")
            year = date_rptd.year 
            print(year)
            print(date_rptd)
            with connection.cursor() as cursor:
                # Βρίσκουμε τον επόμενο διαθέσιμο αριθμό για το συγκεκριμένο Area ID και date_rptd
                query = """
                    SELECT COUNT(*) + 1 
                    FROM Crime_report 
                    WHERE area_id = %s AND EXTRACT(YEAR FROM date_rptd) = %s;
                """
                cursor.execute(query, [area_id, year])
                next_record_number = cursor.fetchone()[0]
                print(next_record_number)
            year = year % 100
            # Δημιουργούμε το DR_NO
            dr_no = f"{year:02}{int(area_id):02}{next_record_number:05}"
            print(dr_no)
            return Response({"dr_no": dr_no}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


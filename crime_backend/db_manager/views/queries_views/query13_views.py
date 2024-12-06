from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

class Query13View(APIView):
    def get(self, request):
        print("Hello")
     
        def parse_time(time_str):
            return datetime.strptime(time_str, '%H:%M').time() if time_str else None

        start_time = parse_time(request.query_params.get('startTime'))
        end_time = parse_time(request.query_params.get('endTime'))
        N = int(request.query_params.get('N'))
        
        if not start_time or not end_time or not N:
            return Response({"error": "Start/End time and N are required."}, status=400)
    
        sql = """
            WITH AuxiliaryTable1 AS(
                SELECT crm_cd.crm_cd AS crime_cd, 
                    crime_chronicle_date_occ as date,
                    wp.weapon_cd AS weapon_cd,
                    cr.area_id AS area_id
                FROM Crime_report AS cr
                JOIN Weapon AS wp ON cr.weapon_cd = wp.weapon_cd
                JOIN Timestamp AS time ON time.timestamp_id = cr.timestamp_id
                JOIN Crime_code AS crm_cd ON cr.crm_cd = crm_cd.crm_cd_id
                WHERE wp.weapon_cd <> -1 AND crm_cd.crm_cd <> -1 AND time.time_occ %s AND %s 
                GROUP BY crm_cd.crm_cd, time.date_occ, wp.weapon_cd, cr.area_id 
                HAVING COUNT(crm_cd.crm_cd) = %s
                ORDER BY crm_cd.crm_cd, time.date_occ, wp.weapon_cd, cr.area_id
            ),
            DR_NO_LIST AS(
                SELECT dr_no
                FROM AuxiliaryTable1
                JOIN Crime_report AS cr ON cr.weapon_cd = weapon_cd AND cr.area_id = area_id
                JOIN Crime_code AS crm_cd ON cr.crm_cd = crm_cd.crm_cd_id AND crm_cd.crm_cd = crime_cd
                JOIN Timestamp AS time ON time.timestamp_id = cr.timestamp_id AND time.date_occ = date
            )
            SELECT DISTINCT cr.dr_no, a.area_name, crm_cd.crm_cd_desc, wp.weapon_desc
            FROM DR_NO_LIST AS dr
            JOIN Crime_report AS cr ON dr.dr_no = cr.dr_no 
            JOIN Area AS a ON a.area_id = cr.area_id 
            JOIN Crime_code AS crm_cd ON cr.crm_cd = crm_cd.crm_cd_id
            JOIN Weapon AS wp ON cr.weapon_cd = wp.weapon_cd
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, [start_time, end_time, N])
                rows = cursor.fetchall()
                
            if not rows:  # Check if the list is empty.
                return Response({"message": "No data available for the given time range."}, status=200)
            
            # Formatting results in JSON.
            results = [{"DR_NO": row[0], "Area name": row[1], "Crime code desc": row[2], "Weapon desc": row[3]} for row in rows]
            return Response(results, status=200)
        
        except Exception as e:
                return Response({"error": str(e)}, status=500)
        


from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

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


class SaveNewCodeView(APIView):
    def post(self, request):
        data = request.data

        try:
            with connection.cursor() as cursor:
                # ---------------------------------------------------------------------
                # ------------------------    Data Parsing    -------------------------
                # ---------------------------------------------------------------------

                # Functions for parsing dates and times
                def parse_date(date_str):
                    return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

                def parse_time(time_str):
                    return datetime.strptime(time_str, '%H:%M').time() if time_str else None

                # Extract data from the request
                dr_no = data.get('DR_NO')
                date_rptd = parse_date(data.get('DateRptd'))
                date_occ = parse_date(data.get('DateOcc'))
                time_occ = parse_time(data.get('TimeOcc'))
                area_id = data.get('AreaCode')
                area_name = data.get('AreaDesc')
                premis_cd = data.get('PremisCd')
                premis_desc = data.get('PremisesDesc')
                crm_cd = data.get('CrmCd')
                crime_code_desc = data.get('Crime_codeDesc')
                crm_cd2 = data.get('CrmCd2') or None
                crm_cd3 = data.get('CrmCd3') or None
                crm_cd4 = data.get('CrmCd4') or None
                weapon_cd = data.get('WeaponUsedCd')
                weapon_desc = data.get('WeaponDesc')
                location = data.get('Location')
                lat = data.get('Latitude')
                lon = data.get('Longitude')
                cross_street = data.get('CrossStreet')
                status_code = data.get('Status')
                status_desc = data.get('StatusDesc')
                rpt_dist_no = data.get('RptDistNo') or None
                mocodes = data.get('Mocodes')
                vict_age = data.get('VictAge')
                vict_sex = data.get('VictSex')
                vict_descent = data.get('VictDescent')

                # Convert types where necessary
                lat = float(lat) if lat else None
                lon = float(lon) if lon else None
                premis_cd = int(premis_cd) if premis_cd else None
                weapon_cd = int(weapon_cd) if weapon_cd else None
                crm_cd = int(crm_cd) if crm_cd else None
                crm_cd2 = int(crm_cd2) if crm_cd2 else None
                crm_cd3 = int(crm_cd3) if crm_cd3 else None
                crm_cd4 = int(crm_cd4) if crm_cd4 else None
                rpt_dist_no = int(rpt_dist_no) if rpt_dist_no else None
                vict_age = int(vict_age) if vict_age else None

                # ---------------------------------------------------------------------
                # Insert data into the -- Area -- table
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Area (area_id, area_name)
                        VALUES (%s, %s)
                        ON CONFLICT (area_id) DO NOTHING
                    """, [area_id, area_name])
                print('line204')
                # ---------------------------------------------------------------------
                # Insert data into the -- Crime_Location -- table
                with connection.cursor() as cursor:
                    # Check if location already exists
                    cursor.execute("""
                        INSERT INTO Crime_Location (location, lat, lon, cross_street)
                        VALUES (%s, %s, %s, %s)
                    """, (location, lat, lon, cross_street) )
                    connection.commit()
                    
                    cursor.execute("""
                        SELECT location_id, location, lat, lon, cross_street
                        FROM Crime_Location 
                        WHERE location = %s AND lat = %s AND lon = %s AND cross_street = %s
                    """, (location, lat, lon, cross_street))
                    location_id = cursor.fetchone()[0]
                    
                    
                print('line224')
                # ---------------------------------------------------------------------
                # Insert data into the -- Status -- table
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Status (status_code, status_desc)
                        VALUES (%s, %s)
                        ON CONFLICT (status_code) DO NOTHING
                    """, [status_code, status_desc])
                    connection.commit()
                print('line233')
                # ---------------------------------------------------------------------
                # Insert data into the -- Premises -- table
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Premises (premis_cd, premis_desc)
                        VALUES (%s, %s)
                        ON CONFLICT (premis_cd) DO NOTHING
                    """, [premis_cd, premis_desc])
                    connection.commit()
                print('line242')
                # ---------------------------------------------------------------------
                # Insert data into the -- Weapon -- table
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Weapon (weapon_cd, weapon_desc)
                        VALUES (%s, %s)
                        ON CONFLICT (weapon_cd) DO NOTHING
                    """, [weapon_cd, weapon_desc])
                    connection.commit()
                print('line251')
                # ---------------------------------------------------------------------
                # Insert data into the -- Crime_code -- table
                # Insert main crime code
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Crime_code (crm_cd, crm_cd_desc)
                        VALUES (%s, %s)
                    """, [crm_cd, crime_code_desc])
                    connection.commit()
                    
                    cursor.execute("""
                        SELECT crm_cd_id FROM Crime_code WHERE crm_cd = %s
                    """, (crm_cd,))
                    crm_cd_id = cursor.fetchone()
                    print('line268')
                    cursor.execute("""
                        SELECT COUNT(*) FROM Crime_code WHERE crm_cd = %s
                    """, (crm_cd2,))
                    exists = cursor.fetchone()[0]

                    if exists == 0: 
                        cursor.execute("""
                            INSERT INTO Crime_code (crm_cd, crm_cd_desc)
                            VALUES (%s, %s)
                        """, [crm_cd2, 'No description'])
                        connection.commit()
                        
                    cursor.execute("""
                        SELECT crm_cd_id FROM Crime_code WHERE crm_cd = %s
                    """, (crm_cd2,))
                    crm_cd2_id = cursor.fetchone()[0]

                    cursor.execute("""
                        SELECT COUNT(*) FROM Crime_code WHERE crm_cd = %s
                    """, (crm_cd3,))
                    exists = cursor.fetchone()[0]

                    if exists == 0: 
                        cursor.execute("""
                            INSERT INTO Crime_code (crm_cd, crm_cd_desc)
                            VALUES (%s, %s)
                        """, [crm_cd3, 'No description'])
                        connection.commit()
                        
                    cursor.execute("""
                        SELECT crm_cd_id FROM Crime_code WHERE crm_cd = %s
                    """, (crm_cd3,))
                    crm_cd3_id = cursor.fetchone()[0]

                    cursor.execute("""
                        SELECT COUNT(*) FROM Crime_code WHERE crm_cd = %s
                    """, (crm_cd4,))
                    exists = cursor.fetchone()[0]

                    if exists == 0: 
                        cursor.execute("""
                            INSERT INTO Crime_code (crm_cd, crm_cd_desc)
                            VALUES (%s, %s)
                        """, [crm_cd4, 'No description'])
                        connection.commit()
                        
                    cursor.execute("""
                        SELECT crm_cd_id FROM Crime_code WHERE crm_cd = %s
                    """, (crm_cd4,))
                    crm_cd4_id = cursor.fetchone()[0]

                print('line319')
                # ---------------------------------------------------------------------
                # Insert data into the -- Timestamp -- table
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Timestamp (date_occ, time_occ)
                        VALUES (%s, %s)
                    """, [date_occ, time_occ])
                    # Retrieve timestamp_id
                    cursor.execute("SELECT timestamp_id FROM Timestamp WHERE date_occ = %s AND time_occ = %s", [date_occ, time_occ])
                    timestamp_id = cursor.fetchone()[0]
                print('line319')
                # ---------------------------------------------------------------------
                # Insert data into the -- Reporting_District -- table
                if rpt_dist_no and area_id:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO Reporting_District (rpt_dist_no, area_id)
                            VALUES (%s, %s)
                            ON CONFLICT (rpt_dist_no) DO NOTHING
                        """, [rpt_dist_no, area_id])
                print('line359')
                # ---------------------------------------------------------------------
                # Insert data into the -- Crime_report -- table
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Crime_report (
                            dr_no, date_rptd, timestamp_id, status_code, premis_cd, rpt_dist_no,
                            area_id, location_id, mocodes, weapon_cd, crm_cd, crm_cd_2, crm_cd_3, crm_cd_4
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, [
                        dr_no, date_rptd, timestamp_id, status_code, premis_cd, rpt_dist_no,
                        area_id, location_id, mocodes, weapon_cd, crm_cd_id,
                        crm_cd2_id, crm_cd3_id, crm_cd4_id
                    ])
                print('line373')
                # ---------------------------------------------------------------------
                # Insert data into the -- Victim -- table
                if vict_age or vict_sex or vict_descent:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO Victim (
                                dr_no, vict_age, vict_sex, vict_descent
                            ) VALUES (%s, %s, %s, %s)
                        """, [
                            dr_no, vict_age, vict_sex, vict_descent
                        ])
                print('line385')
                return Response({'message': 'Record inserted successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



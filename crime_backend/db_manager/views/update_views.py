from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response

class UpdateView(APIView):
    def post(self, request):
        dr_no = request.data.get('DR_NO')
        if not dr_no:
            return Response({"error": "DR_NO is required"}, status=400)
        print(request.data.items() )
        # Identify fields to be updated.
        fields_to_update = {key: value for key, value in request.data.items() if key != 'DR_NO' and value is not None}
        if not fields_to_update:
            return Response({"error": "No fields to update"}, status=400)
        print(fields_to_update)
        # Δημιουργία log
        changes_log = [{"field": key, "new_value": value} for key, value in fields_to_update.items()]

        data_tables = {
            "DateRptd": "Crime_report",
            "DateOcc": "Timestamp",
            "TimeOcc": "Timestamp",
            "AreaCode": "Area",
            "AreaDesc": "Area",
            "PremisCd": "Premises",
            "PremisesDesc": "Premises",
            "CrmCd": "Crime_code",
            "Crime_codeDesc": "Crime_code",
            "CrmCd2": "Crime_report",
            "CrmCd3": "Crime_report",
            "CrmCd4": "Crime_report",
            "WeaponUsedCd": "Weapon",
            "WeaponDesc": "Weapon",
            "Location": "Crime_Location",
            "Latitude": "Crime_Location",
            "Longitude": "Crime_Location",
            "CrossStreet": "Crime_Location",
            "Status": "Status",
            "StatusDesc": "Status",
            "RptDistNo": "Crime_report",
            "Mocodes": "Crime_report",
            "VictAge": "Victim",
            "VictSex": "Victim",
            "VictDescent": "Victim",
        }

        tables_data = {
            "Area" : [],
            "Crime_Location" : [],
            "Status": [],
            "Premises": [],
            # "Reporting_District": [],
            "Crime_code": [],
            "Weapon": [],
            "Timestamp": [],
            "Crime_report": [],
            "Victim": []
        }

        correctedField ={
            "DateRptd": "date_rptd",
            "DateOcc": "date_occ",
            "TimeOcc": "time_occ",
            "AreaCode": "area_id",
            "AreaDesc": "area_name",
            "PremisCd": "premis_cd",
            "PremisesDesc": "premis_desc",
            "WeaponUsedCd": "weapon_cd",
            "WeaponDesc": "weapon_desc",
            "Location": "location",
            "Latitude": "lat",
            "Longitude": "lon",
            "CrossStreet": "cross_street",
            "Status": "status_code",
            "StatusDesc": "status_desc",
            "RptDistNo": "rpt_dist_no",
            "Mocodes": "mocodes",
            "VictAge": "vict_age",
            "VictSex": "vict_sex",
            "VictDescent": "vict_descent", 
            "CrmCd": "crm_cd",
            "Crime_codeDesc": "crm_cd_desc",    
        }

        # Κατανομή των δεδομένων στο tables_data
        for field, value in fields_to_update.items():
            table = data_tables.get(field)  # Βρες σε ποιον πίνακα ανήκει το πεδίο
            if table:
                tables_data[table].append({field: value})

        print("Tables Data:", tables_data)

        # 7. Εκτέλεση των δυναμικών ενημερώσεων params= [fields_to_update[key] for key in field.keys()]
        try:
            with connection.cursor() as cursor:

                query = """ 
                    SELECT dr_no, date_rptd, timestamp_id, status_code, 
                           premis_cd, rpt_dist_no, area_id, location_id, 
                           mocodes, weapon_cd, crm_cd, crm_cd_2, crm_cd_3, 
                           crm_cd_4
                    FROM 
                        Crime_report 
                    WHERE 
                        dr_no = %s
                """
                cursor.execute(query, [dr_no])
                row = cursor.fetchone()
                print(row)
                print("line110")
                total_paramas_crm_rpt = {}
                for table, fields in tables_data.items():

                    conditions = []
                    for field in fields:
                        for key in field.keys():
                            conditions.append(f"{correctedField[key]} = %s")

                    set_clause = " AND ".join(conditions)


                    print(f"line116: {set_clause}")
                    if table == "Area":
                        cursor.execute("""
                            SELECT COUNT(*) FROM Area WHERE area_id = %s
                        """, (fields_to_update["AreaCode"],))
                        exists = cursor.fetchone()[0]

                        if exists == 0: 
                            params = []
                            for field in fields:
                                params += [fields_to_update[key] for key in field.keys()]

                            cursor.execute("""
                                INSERT INTO Area (area_id, area_name)
                                VALUES (%s, %s)
                            """, params)
                            connection.commit()

                        total_paramas_crm_rpt[correctedField["AreaCode"]] = fields_to_update["AreaCode"]
                        print(f"line117 {total_paramas_crm_rpt[correctedField['AreaCode']]}")

                    # print("Crime_Location")
                    elif table == "Crime_Location":
                        print("Crime_Location")
                        params = []
                        for field in fields:
                            params += [fields_to_update[key] for key in field.keys()]
                        params.append(row[7])   # location_id
                        print(params)
                        print(f"{set_clause}")
                        sql = """
                            UPDATE Crime_Location 
                            SET {}
                            WHERE location_id = %s
                        """.format(set_clause)
                        cursor.execute(sql, params)
                        print("line143")

                    elif table == "Status":
                            cursor.execute("""
                                SELECT COUNT(*) FROM Status WHERE status_code = %s
                            """, (fields_to_update["Status"],))
                            exists = cursor.fetchone()[0]

                            if exists == 0: 
                                params = []
                                for field in fields:
                                    params += [fields_to_update[key] for key in field.keys()]
                                cursor.execute("""
                                    INSERT INTO Status (status_code, status_desc)
                                    VALUES (%s, %s)
                                """, params)
                                connection.commit()

                            total_paramas_crm_rpt[correctedField["Status"]] = fields_to_update["Status"]
                            print("line160")


                    elif table == "Premises":
                            cursor.execute("""
                                SELECT COUNT(*) FROM Premises WHERE premis_cd = %s
                            """, (fields_to_update["PremisCd"],))
                            exists = cursor.fetchone()[0]

                            if exists == 0: 
                                params = []
                                for field in fields:
                                    params += [fields_to_update[key] for key in field.keys()]
                                cursor.execute("""
                                    INSERT INTO Premises (premis_cd, premis_desc)
                                    VALUES (%s, %s)
                                """, params)
                                connection.commit()

                            total_paramas_crm_rpt[correctedField["PremisCd"]] = fields_to_update["PremisCd"]
                            print("line178")

                    elif table == "Crime_code":
                            cursor.execute("""
                                SELECT COUNT(*) FROM Crime_code WHERE crm_cd = %s
                            """, (fields_to_update["CrmCd"],))
                            exists = cursor.fetchone()[0]

                            if exists == 0: 
                                params = []
                                for field in fields:
                                    params += [fields_to_update[key] for key in field.keys()]
                                cursor.execute("""
                                    INSERT INTO Crime_code (crm_cd, crm_cd_desc)
                                    VALUES (%s, %s)
                                """, params)
                                connection.commit()

                            cursor.execute("""
                                SELECT crm_cd_id FROM Crime_code WHERE crm_cd = %s
                            """, (fields_to_update["CrmCd"],))
                            crm_cd_id = cursor.fetchone()[0]
                            
                            total_paramas_crm_rpt[correctedField["CrmCd"]] = fields_to_update["CrmCd"]
                            print("line200")

                    elif table == "Weapon":
                            cursor.execute("""
                                SELECT COUNT(*) FROM Weapon WHERE weapon_cd = %s
                            """, (fields_to_update["WeaponUsedCd"],))
                            exists = cursor.fetchone()[0]

                            if exists == 0: 
                                params = []
                                for field in fields:
                                    params += [fields_to_update[key] for key in field.keys()]
                                cursor.execute("""
                                    INSERT INTO Weapon (weapon_cd, weapon_desc)
                                    VALUES (%s, %s)
                                """, params)
                                connection.commit()

                            total_paramas_crm_rpt[correctedField["WeaponUsedCd"]] = fields_to_update["WeaponUsedCd"]
                            print("line217")

                    elif table == "Timestamp":
                            params = []
                            for field in fields:
                                params += [fields_to_update[key] for key in field.keys()]
                            if len(params) == 1:
                                key = list(field.keys())[0]

                                cursor.execute("""
                                    SELECT date_occ, time_occ FROM Timestamp WHERE timestamp_id = %s 
                                """, (row[2],))
                                date_occ, time_occ = cursor.fetchone()[0]
                                
                                if key == "DateOcc":
                                    params = [fields_to_update[key], time_occ]
                                else:
                                    params = [date_occ, fields_to_update[key]]

                            
                            cursor.execute("""
                                SELECT COUNT(*) FROM Timestamp WHERE date_occ = %s AND time_occ = %s
                            """, params)
                            exists = cursor.fetchone()[0]

                            if exists == 0: 
                                params = []
                                for field in fields:
                                    params += [fields_to_update[key] for key in field.keys()]

                                cursor.execute("""
                                    INSERT INTO Timestamp (date_occ, time_occ)
                                    VALUES (%s, %s)
                                """, params)
                                connection.commit()

                            cursor.execute("""
                                SELECT timestamp_id FROM Timestamp WHERE date_occ = %s AND time_occ = %s
                            """, params)
                            timestamp_id = cursor.fetchone()[0]

                            total_paramas_crm_rpt['timestamp_id'] = timestamp_id
                            print("line254")

                            if table == "Victim":
                                params = []
                                for field in fields:
                                    params += [fields_to_update[key] for key in field.keys()]
                                params += [dr_no]
                                cursor.execute(f"""
                                    UPDATE Victim
                                    SET {set_clause}
                                    WHERE dr_no = %s
                                """, params)
                                print("line264")


                    elif table == "Crime_report":
                            for key in field.keys():
                                
                                if key == "CrmCd2" or key == "CrmCd3"  or key == "CrmCd4":
                                    
                                    cursor.execute("""
                                        SELECT COUNT(*) FROM Crime_code WHERE crm_cd = %s
                                    """, (fields_to_update[key],))
                                    exists = cursor.fetchone()[0]

                                    if exists == 0: 
                                        params = [fields_to_update[key]]
                                        params += ["No description"]
                                        cursor.execute("""
                                            INSERT INTO Crime_code (crm_cd, crm_cd_desc)
                                            VALUES (%s, %s)
                                        """, params)
                                        connection.commit()

                                    cursor.execute("""
                                        SELECT crm_cd_id FROM Crime_code WHERE crm_cd = %s
                                    """, (fields_to_update[key],))
                                    crm_cd_id = cursor.fetchone()[0]

                                    if key == "CrmCd2": total_paramas_crm_rpt["crm_cd_2"] = crm_cd_id
                                    elif key == "CrmCd3": total_paramas_crm_rpt["crm_cd_3"] = crm_cd_id
                                    elif key == "CrmCd4": total_paramas_crm_rpt["crm_cd_4"] = crm_cd_id
                                
                                total_paramas_crm_rpt[correctedField[key]] = fields_to_update[key]
                                print("line296")
                           
                set_clause = ', '.join([f"{key} = %s" for key in total_paramas_crm_rpt.keys()])
                params = list(total_paramas_crm_rpt.values())
                params += [dr_no]
                query = """ 
                    UPDATE Crime_report
                    SET {set_clause}
                    WHERE dr_no = %s
                """
                cursor.execute(query, params)
                        
            # Αποθήκευση του log
            # (Αν έχετε κάποιο πίνακα `UpdateLog` μπορείτε να το αποθηκεύσετε εκεί)
            print("Update Log:", changes_log)  # Ή αποθηκεύστε το σε βάση δεδομένων

            return Response({"message": "Record updated successfully", "log": changes_log}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

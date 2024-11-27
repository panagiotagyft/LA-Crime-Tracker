from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response

class Query9View(APIView):
    def get(self, request):

        try:
            print("Hello")
            with connection.cursor() as cursor:

                sql="""
                    WITH AgeBuckets AS (
                        -- Step 1: Bucket victim ages into 5-year intervals
                        SELECT vict_age, cr.weapon_cd AS weapon_cd, 
                        FLOOR(vict_age / 5) * 5 || ' ≤ x < ' || (FLOOR(vict_age / 5) * 5 + 5) AS age_group -- Create age group labels
                        FROM  Victim v
                        JOIN Crime_report AS cr ON cr.dr_no = v.dr_no
                        WHERE vict_age <> -1 AND cr.weapon_cd <> -1
                    ),
                    WeaponOccCount AS (
                        -- Step 2: Count occurrences of each weapon type per age group
                        SELECT age_group, weapon_cd, COUNT(*) AS weapon_count
                        FROM AgeBuckets
                        GROUP BY age_group, weapon_cd
                    ),
                    MostWeapon AS (
                        -- Step 3: Find the maximum weapon count for each age group
                        SELECT age_group, MAX(weapon_count) AS max_weapon_count
                        FROM WeaponOccCount
                        GROUP BY age_group
                    )
                    -- Step 4: Fetch the weapon(s) with the maximum count for each age group
                    SELECT wc.age_group, wc.weapon_cd AS most_common_weapon, wc.weapon_count AS occurrence_count
                    FROM WeaponOccCount AS wc
                    JOIN MostWeapon AS mw ON wc.age_group = mw.age_group AND wc.weapon_count = mw.max_weapon_count;
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
        


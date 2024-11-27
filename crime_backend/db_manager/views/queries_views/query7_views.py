from django.db import connection 
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

class Query7View(APIView):
    def get(self, request):
        
        def parse_date(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        start_date = parse_date(request.query_params.get('startDate'))
        end_date = parse_date(request.query_params.get('endDate'))
        
        if not start_date or not end_date:
            return Response({"Error": "Start/End date are required!"}, status=400)

        try:
            with connection.cursor() as cursor:
                sql = """
                    -- Step 1: Generate all possible unique pairs of crime codes from the Crime_code table
                    WITH AllPairs AS (
                        SELECT 
                            c1.crm_cd AS crime1, c1.crm_cd_id AS crime1_id, -- The first crime code in the pair
                            c2.crm_cd AS crime2, c2.crm_cd_id AS crime2_id  -- The second crime code in the pair
                        FROM Crime_code c1
                        JOIN Crime_report cr2 ON cr1.dr_no = cr2.dr_no -- Match crimes in the same report
                        WHERE 
                            c1.crm_cd < c2.crm_cd -- Ensure unique pairs by ordering (e.g., include (111, 222) but exclude (222, 111))
                    ),
                    -- Step 2: Calculate the frequency of each pair by area
                    PairFrequencyByArea AS (
                        SELECT
                            ap.crime1, -- The first crime in the pair
                            ap.crime2, -- The second crime in the pair
                            cr.area_id, -- The area where the pair occurred
                            COUNT(*) AS pair_count -- Count how many times this pair occurred in this area
                        FROM AllPairs AS ap
                        JOIN Crime_report AS cr ON (
                                -- Check if both crimes in the pair are present in any of the crime report columns
                                (ap.crime1_id = cr.crm_cd OR ap.crime1_id = cr.crm_cd_2 OR ap.crime1_id = cr.crm_cd_3 OR ap.crime1_id = cr.crm_cd_4)
                                AND
                                (ap.crime2_id = cr.crm_cd OR ap.crime2_id = cr.crm_cd_2 OR ap.crime2_id = cr.crm_cd_3 OR ap.crime2_id = cr.crm_cd_4)
                            )
                        WHERE cr.date_rptd BETWEEN %s AND %s
                        GROUP BY ap.crime1, ap.crime2, cr.area_id -- Group results by area and pair
                    )
                    -- Step 3: Combine area names with pair frequency data and sort results
                    SELECT 
                        a.area_name, -- The name of the area
                        pfba.crime1,   -- The first crime in the pair
                        pfba.crime2,   -- The second crime in the pair
                        pfba.pair_count -- The number of times this pair occurred in this area
                    FROM PairFrequencyByArea pfba
                    JOIN Area AS a ON a.area_id = pfba.area_id
                    WHERE pfba.crime1 <> -1 AND pfba.crime2 <> -1
                    ORDER BY pfba.pair_count DESC -- Sort by the number of occurrences in descending order
                    LIMIT 1;
                """
                cursor.execute(sql, [start_date, end_date])
                rows = cursor.fetchall()
            
            if not rows:  # Check if the list is empty.
                return Response({"message": "No data available for the given time range."}, status=200)
            
            # Formatting results in JSON.
            results = [{"Area name": row[0], "Crime 1": row[1], "Crime 2": row[2], "Pair Count": row[3]} for row in rows]
            return Response(results, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)

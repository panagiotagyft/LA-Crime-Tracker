from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CrimeCode, CrimeReport, Premise, ReportingDistrict, Status, Timestamp, Weapon
from .models import User
from .serializer import CrimeCodeSerializer
from .serializer import UserSerializer

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Create your views here.

class Index(View):
    def get(self, request):
        return render(request, "api/index.html")    #!add this!!!!, or don't
    
@api_view(["GET"])
def get_users():
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_user(request, user_id):
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET, PUT, DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["POST"])
def add_user(request):
    try:
        data = json.loads(request.body)  # Parse JSON data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        print(request.body.decode("utf-8"))
        # Validation
        if password != confirm_password:
            return JsonResponse({"errors": {"password": ["Passwords do not match."]}}, status=400)

        # Logic to create the user
        print("So far so good!")
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("User created successfully!")
    

        return JsonResponse({"message": "User created successfully!"}, status=201)
    except Exception as e:
        return JsonResponse({"errors": {"non_field_errors": [str(e)]}}, status=400)


# ----------------------------------------------------------


@api_view(["GET"])
def reports_per_crime_code_in_time_range(request):
    # Get query parameters
    print("This is the request: ", request)
    print("data is: ", request.data)
    start_time = request.GET.get("start_time")  # e.g., "0000"
    end_time = request.GET.get("end_time")  # e.g., "2359"

    # Validate input
    if not start_time or not end_time:
        return JsonResponse({"error": "start_time and end_time are required parameters."}, status=400)

    if not (start_time.isdigit() and end_time.isdigit() and len(start_time) == 4 and len(end_time) == 4):
        return JsonResponse({"error": "Time must be in military format (e.g., 0000, 2359)."}, status=400)

    # Define the query
    query = """
        SELECT crm_cd, COUNT(*) AS report_count
        FROM crime_incident_crime_code AS code
        JOIN crime_report AS report ON code.dr_no = report.dr_no
        WHERE report.time_occ BETWEEN %s AND %s
        GROUP BY crm_cd
        ORDER BY report_count DESC;
    """

    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(query, [start_time, end_time])
        results = cursor.fetchall()

    # Format the results
    formatted_results = [{"crime_code": row[0], "report_count": row[1]} for row in results]

    # Return the results as JSON
    return JsonResponse({
        "start_time": start_time,
        "end_time": end_time,
        "results": formatted_results,
        "total_reports": sum(row[1] for row in results)
    })
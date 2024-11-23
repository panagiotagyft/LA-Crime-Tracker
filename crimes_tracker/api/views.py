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
        return render(request, "api/index.html")    #!add this!!!!
    
@api_view(["GET"])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# @api_view(["POST"])
# def add_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# @require_http_methods(["POST"])
# def add_user(request):
#     print("Incoming Data:", request.body)
#     print("Incoming Data Type:", type(request.body))
#     print(request.body.decode("utf-8"))
#     try:
#         data = json.loads(request.body)
#         print("Incoming Data:", data)  # Debugging
#         return JsonResponse({"message": "User added successfully"}, status=201)
#     except Exception as e:
#         print("Error:", e)
#         return JsonResponse({"error": str(e)}, status=400)

# @csrf_exempt
# @require_http_methods(["POST"])
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
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
    
        print("User created successfully!")

        return JsonResponse({"message": "User created successfully!"}, status=201)
    except Exception as e:
        return JsonResponse({"errors": {"non_field_errors": [str(e)]}}, status=400)

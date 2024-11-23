from rest_framework import serializers
from .models import (CrimeCode, CrimeReport, Premise, ReportingDistrict, Status, Timestamp, Weapon)
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
        
class CrimeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeCode
        fields = "__all__"
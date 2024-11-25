from rest_framework import serializers
from .models import (Area, CrimeLocation, Status, Premise, ReportingDistrict, Timestamp, CrimeCode, Weapon, CrimeReport, Victim)
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"
        
class CrimeLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeLocation
        fields = "__all__"

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class PremiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premise
        fields = "__all__"


class ReportingDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportingDistrict
        fields = "__all__"


class TimestampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timestamp
        fields = "__all__"
        
class CrimeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeCode
        fields = "__all__"
        
class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = "__all__"
        
class CrimeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeReport
        fields = "__all__"


class VictimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victim
        fields = "__all__"
        
        
        
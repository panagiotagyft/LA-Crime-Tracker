from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)  # Προσθήκη confirm_password

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # Έλεγχος αν ο password και confirm_password είναι ίδιοι
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Αφαιρούμε το confirm_password, γιατί δεν το χρειαζόμαστε για την αποθήκευση
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)  # Δημιουργία token για τον χρήστη
        return user

from rest_framework import serializers
from .models import CustomUser ,Employer_Profile,Employee_Details
#
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email']


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer_Profile
        fields = '__all__'

class EmployeeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Details
        fields = '__all__'


class GetEmployeeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Details
        fields = '__all__'


class GetEmployerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer_Profile
        fields = '__all__'
from rest_framework import serializers
from .models import *

class HealthGoalSerializers(serializers.ModelSerializer):
    class Meta:
        model  = HealthGoal
        fields = '__all__'

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model  = Profile
        fields = '__all__'

class DiagonsisSerializers(serializers.ModelSerializer):
    class Meta:
        model  = Diagonsis
        fields = '__all__'

class SymptomsSerializers(serializers.ModelSerializer):
    class Meta:
        model  = Symptoms
        fields = '__all__'

class NimbouserSerializers(serializers.ModelSerializer):
    class Meta:
        model = NimboUser
        fields = '__all__'

class HealthstyleSerializers(serializers.ModelSerializer):
    class Meta:
        model = HealthStyle
        fields = '__all__'

class AdduserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Add_user
        fields = '__all__'
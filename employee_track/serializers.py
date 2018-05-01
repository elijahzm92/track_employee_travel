from rest_framework import serializers
from django.contrib.auth.models import User

from . import models

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)

class EmployeeLocationSerializer(serializers.ModelSerializer):
    employee = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'employee', 'latitude', 'longitude','created_at',)
        model = models.Location

class LocationSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        fields = ('id', 'employee', 'latitude', 'longitude','created_at',)
        model = models.Location        
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from math import radians, cos, sin, asin, sqrt

from . import models
from . import serializers




class EmployeeLocationList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.EmployeeLocationSerializer

    def get_queryset(self, *args, **kwargs):
        return models.Location.objects.all().filter(employee=self.request.user)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.EmployeeLocationSerializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeLocationDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class=serializers.EmployeeLocationSerializer

    def get_queryset(self):
        return models.Location.objects.all().filter(employee=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.LocationSerializer(queryset)
        return Response(serializer.data)    

class LocationList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)
    serializer_class=serializers.LocationSerializer
    queryset = models.Location.objects.all()

class SpecificEmployeeLocationList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.EmployeeLocationSerializer

    def get_queryset(self):
        return models.Location.objects.all().filter(employee__username=self.kwargs['username'])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.EmployeeLocationSerializer(queryset, many=True)
        return Response(serializer.data)


class SpecificEmployeeDistanceTravelled(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)



    def get(self, request, *args, **kwargs):
        username = self.request.query_params.get('username', None)

        if username is None:
            return Response({
                'error': "username not found in query params"
            })

        try:
            employee = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            employee = None

        if employee is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        date_before = self.request.query_params.get('date_lte', None)
        date_after = self.request.query_params.get('date_gte', None)

        if date_before is not None and date_after is not None:
            #todo add validations for the date_before and date_after field
            employee_locations = models.Location.objects.filter(employee__username=username,
                                                    created_at__gte=date_after, created_at__lte=date_before)
        else:
            employee_locations = models.Location.objects.filter(employee__username=username).order_by('-created_at')
            if len(employee_locations) > 0:
                employee_location = employee_locations[0]
            employee_locations = models.Location.objects.filter(employee__username=username, created_at__year=employee_location.created_at.year,
                                                                created_at__month=employee_location.created_at.month,
                                                                created_at__day=employee_location.created_at.day)

        locations = []
        for employee_location in employee_locations:
            locations.append({"latitude": employee_location.latitude, "longitude": employee_location.longitude})

        distance_travelled = 0
        if len(locations) > 1:
            temp=locations[0]
            for location in locations[1:]:
                d=self.haversine(temp["longitude"],temp["latitude"],location["longitude"],location["latitude"])
                temp=location
                distance_travelled+=d



        return Response({
            "locations": locations,
            "distance_travelled": distance_travelled
        })

    def haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r



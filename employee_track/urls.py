from django.urls import path

from . import views

urlpatterns = [
    path('locations/', views.LocationList.as_view()),
    path('locations/<int:pk>/', views.LocationDetail.as_view()),
    path('me/locations/', views.EmployeeLocationList.as_view()),
    path('employees/<username>/locations/', views.SpecificEmployeeLocationList.as_view()),
    path('employee/distance-travelled/', views.SpecificEmployeeDistanceTravelled.as_view()),
    path('me/locations/<int:pk>/', views.EmployeeLocationDetail.as_view()),
]
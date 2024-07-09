from django.urls import path
from . import views
from .views import UserUpdateAPIView,EmployerProfileEditView,UserDeleteAPIView,EmployeeDetailsUpdateAPIView
from django.urls import include, path
from rest_framework import routers
#from .views import fetch_and_store_data, AttendanceCheckView

urlpatterns =[

    path("register", views.register, name="register"),
    path("login",views.login, name="login"),
    path('logout',views.logout,name='logout'),
    path('employer-profile/', views.EmployerProfile, name='employer_profile'),
    path('employee_details/', views.EmployeeDetails, name='employee_details'),
    path('employee_details/<int:employee_id>/',EmployeeDetailsUpdateAPIView.as_view(), name='Employee_Details_UpdateAPIView'),
    path('<str:username>/', UserUpdateAPIView.as_view(),name='User-Update-API-View'),
    path('employer-profile/<int:employer_id>/',EmployerProfileEditView.as_view(),name='Employer_Profile_UpdateAPIView'),
    path('delete/<str:username>/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('getemployeedetails/<int:employer_id>/', views.get_employee_by_employer_id, name='employee-by-employer-id'),
    path('getemployerdetails/<int:employer_id>/', views.get_employer_details, name='employer-detail-by-employer-id'),
    
]
from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.userDashboard, name='userDashboard'),
    path('employee/', views.employeeDashboard, name='employeeDashboard'),
    path('user/profile/', views.profile, name='profile'),
    path('user/education/', views.education, name='education'),
    path('user/skill/', views.skill, name='skill'),
    path('user/experience/', views.experience, name='experience'),
    path('employee/userlist/', views.userlist, name='userlist'),
    path('employee/viewuser/<int:id>', views.viewuser, name='viewuser'),
]


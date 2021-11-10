from django.urls import path
from . import views

urlpatterns = [
    path('employee-vacancy', views.vacancy, name='vacancy'),
    path('create-vacancy/', views.createvacancy, name='create-vacancy'),
    path('delete/<int:id>', views.deletevacancy, name='delete-vacancy'),
    path('view-vacancy/<int:id>', views.viewvacancy, name='view-vacancy'),
    path('edit-vacancy/<int:id>', views.editvacancy, name='edit-vacancy'),
    path('user-vacancy/', views.userVacancy, name='user-vacancy'),
    path('view-user-vacancy/<int:id>', views.viewuservacancy, name='view-user-vacancy'),
]
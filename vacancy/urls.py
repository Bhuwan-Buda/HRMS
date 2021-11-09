from django.urls import path
from . import views

urlpatterns = [
    path('', views.vacancy, name='vacancy'),
    path('create-vacancy/', views.createvacancy, name='create-vacancy'),
    path('delete/<int:id>', views.deletevacancy, name='delete-vacancy'),
    path('view-vacancy/<int:id>', views.viewvacancy, name='view-vacancy'),
    path('edit-vacancy/<int:id>', views.editvacancy, name='edit-vacancy'),
]
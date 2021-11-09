from django.urls import path
from . import views


urlpatterns = [
    path('vacancy/', views.vacancy, name='vacancy'),
    path('vacancy/create-vacancy/', views.createvacancy, name='create-vacancy'),
    path('vacancy/delete/<int:id>', views.deletevacancy, name='delete-vacancy'),
    path('vacancy/view-vacancy/<int:id>', views.viewvacancy, name='view-vacancy'),
    path('vacancy/edit-vacancy/<int:id>', views.editvacancy, name='edit-vacancy'),
]
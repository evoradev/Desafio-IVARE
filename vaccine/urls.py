from django.urls import path
from . import views

urlpatterns = [
    path('vaccines/', views.vaccine_list_create),
    path('vaccines/<int:pk>/', views.vaccine_detail),
]

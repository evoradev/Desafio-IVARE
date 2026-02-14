from django.urls import path
from . import views

urlpatterns = [
    path('pets/', views.pet_list_create),
    path('pets/<int:pk>/', views.pet_detail),
]

from django.urls import include, path
from . import views
from .views import PetVaccinationViewSet
from rest_framework.routers import DefaultRouter

# Sem adaptação para o viewset 
#urlpatterns = [
#    path('pets/', views.pet_list_create),
#    path('pets/<int:pk>/', views.pet_detail),
#]

# Com adaptação para o viewset
router = DefaultRouter()
router.register(r'pets', views.PetViewSet, basename='pets')
router.register(r'pet-vaccinations', PetVaccinationViewSet, basename='pet-vaccinations')
urlpatterns = [
    path('', include(router.urls)),
]
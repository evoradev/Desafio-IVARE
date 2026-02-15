from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

#urlpatterns = [
#    path('vaccines/', views.vaccine_list_create),
#    path('vaccines/<int:pk>/', views.vaccine_detail),
#]

router = DefaultRouter()
router.register(r'vaccines', views.VaccineViewSet, basename='vaccines') # restrições aplicadas na viewset, usando jwt para controle de acesso. É permitido visualizar sem JWT mas não criar.
urlpatterns = [
    path('', include(router.urls)),
]

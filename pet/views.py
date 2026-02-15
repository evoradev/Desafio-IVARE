from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Pet, PetVaccination
from .serializer import PetSerializer, PetVaccinationSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

#  FORMA TRADICIONAL DE CRIAR AS VIEWS, SEM USAR VIEWSETS OU GENERIC VIEWS DO DRF
# @api_view(['GET', 'POST'])
# def pet_list_create(request):
#     if request.method == 'GET':
#         pets = Pet.objects.all()
#         serializer = PetSerializer(pets, many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         serializer = PetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PATCH', 'DELETE'])
# def pet_detail(request, pk):
#     pet = get_object_or_404(Pet, pk=pk)
#
#     if request.method == 'GET':
#         serializer = PetSerializer(pet)
#         return Response(serializer.data)
#
#     if request.method == 'PATCH':
#         serializer = PetSerializer(pet, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         pet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     
# @api_view(['GET', 'POST'])
# def petVaccination_create(request):
#     if request.method == 'GET':
#         petVaccination = PetVaccination.objects.all()
#         serializer = PetVaccinationSerializer(petVaccination, many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         serializer = PetVaccinationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     
# @api_view(['GET', 'PATCH', 'DELETE'])
# def petVaccination_detail(request, pk):
#     petVaccination = get_object_or_404(PetVaccination, pk=pk)
#
#     if request.method == 'GET':
#         serializer = PetVaccinationSerializer(petVaccination)
#         return Response(serializer.data)
#
#     if request.method == 'PATCH':
#         serializer = PetVaccinationSerializer(petVaccination, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         petVaccination.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Usando VIEWSETS DO DRF, que é uma forma mais rápida e prática de criar as views, pois já vem com as operações básicas de CRUD implementadas.

class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Pet.objects.all().order_by('-created_at')


class PetVaccinationViewSet(ModelViewSet):
    queryset = PetVaccination.objects.all()
    serializer_class = PetVaccinationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return PetVaccination.objects.select_related(
            'pet',
            'vaccine'
        ).order_by('-application_date')

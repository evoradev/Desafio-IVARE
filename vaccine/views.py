from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Vaccine
from .serializer import VaccineSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Sem VIEWSET
# @api_view(['GET', 'POST'])
# def vaccine_list_create(request):
#     if request.method == 'GET':
#         vaccines = Vaccine.objects.all()
#         serializer = VaccineSerializer(vaccines, many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         serializer = VaccineSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PATCH', 'DELETE'])
# def vaccine_detail(request, pk):
#     vaccine = get_object_or_404(Vaccine, pk=pk)
#
#     if request.method == 'GET':
#         serializer = VaccineSerializer(vaccine)
#         return Response(serializer.data)
#
#     if request.method == 'PATCH':
#         serializer = VaccineSerializer(vaccine, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         vaccine.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Com VIEWSET

class VaccineViewSet(ModelViewSet):
    serializer_class = VaccineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Vaccine.objects.all().order_by("-created_at")

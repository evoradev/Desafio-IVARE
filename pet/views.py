from rest_framework.decorators import api_view, action
from django.contrib.auth.models import User
from .models import Pet, PetVaccination
from .serializer import PetSerializer, PetVaccinationSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Usuário só enxerga seus próprios pets
        return Pet.objects.filter(
            owner=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        # Define automaticamente o dono como usuário logado
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        # Impede editar pet de outro usuário
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this pet.")
        serializer.save()

    def perform_destroy(self, instance):
        # Impede deletar pet de outro usuário
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this pet.")
        instance.delete()


class PetVaccinationViewSet(ModelViewSet):
    serializer_class = PetVaccinationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Só vacinações de pets do usuário logado
        return PetVaccination.objects.select_related(
            'pet',
            'vaccine'
        ).filter(
            pet__owner=self.request.user
        ).order_by('-application_date')

    def perform_create(self, serializer):
        pet = serializer.validated_data.get("pet")

        if pet.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to add vaccination to this pet."
            )

        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.pet.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to edit this vaccination."
            )

        serializer.save()

    def perform_destroy(self, instance):
        if instance.pet.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to remove this vaccination."
            )

        instance.delete()

# Essa forma não é segura pois permite todas as operações por qualquer user. Comentado caso queira utilizar para testes, mas não é o ideal. Deixarei o ideal logo abaixo.
#class UserViewSet(ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    permission_classes = [AllowAny]

# ViewSet padrão para User
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    # Bloqueia listagem
    def list(self, request, *args, **kwargs):
        return Response(
            {"detail": "You cannot list all users."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    # Bloqueia retrieve por ID (opcional agora)
    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"detail": "Use /users/me/"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    # Bloqueia delete
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Deletion of user is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    # Endpoint /me/ para o usuário acessar e editar seus próprios dados
    @action(detail=False, methods=["get", "patch"])
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        if request.method == "PATCH":
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

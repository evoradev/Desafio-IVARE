from rest_framework import serializers
from vaccine.models import Vaccine
from .models import Pet, PetVaccination

class PetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'pet_type', 'owner',
            'description', 'is_published', 'vaccines',
            'created_at', 'updated_at', 'is_vaccinated',
        ]
        

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    updated_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    
    def validate(self, attrs):

        GENERIC_TYPES = {
            Pet.PetType.EXOTIC,
            Pet.PetType.AQUATIC_ANIMAL,
            Pet.PetType.HOUSE_ANIMAL,
            Pet.PetType.FARM_ANIMAL,
        }

        pet_type = attrs.get(
            "pet_type",
            getattr(self.instance, "pet_type", None)
        )

        description = attrs.get(
            "description",
            getattr(self.instance, "description", None)
        )

        if pet_type in GENERIC_TYPES and not description:
            raise serializers.ValidationError({
                "description": (
                    'Description is required for generic animal types '
                    'like "EXOTIC", "AQUATIC_ANIMAL", '
                    '"HOUSE_ANIMAL" or "FARM_ANIMAL".'
                )
            })

        super_validate = super().validate(attrs)
        return super_validate
    
class PetVaccinationSerializer(serializers.ModelSerializer):
    # Para mostrar no GET
    vaccine_name = serializers.CharField(
        source='vaccine.name',
        read_only=True
    )

    # Para enviar no POST
    vaccine = serializers.PrimaryKeyRelatedField(
        queryset=Vaccine.objects.all(),
        write_only=True
    )

    class Meta:
        model = PetVaccination
        fields = [
            'id',
            'pet',
            'vaccine',        # usado só no POST
            'vaccine_name',   # mostrado só no GET
            'application_date',
            'number_of_aplications',
            'batch_number',
            'veterinarian_name',
            'observations',
            'created_at',
        ]

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )
    
    application_date = serializers.DateField(
        format="%Y-%m-%d",
        read_only=True,
    )

    def validate(self, attrs):
        pet = attrs.get(
            "pet",
            getattr(self.instance, "pet", None)
        )

        vaccine = attrs.get(
            "vaccine",
            getattr(self.instance, "vaccine", None)
        )

        errors = {}

        if not pet or not pet.is_published:
            errors["pet"] = "Pet não existe ou não está publicado."

        if not vaccine or not vaccine.is_published:
            errors["vaccine"] = "Vacina não existe ou não está publicada."

        if errors:
            raise serializers.ValidationError(errors)

        super_validate = super().validate(attrs)
        return super_validate
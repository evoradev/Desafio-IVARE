from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'pet_type', 'owner',
            'description', 'is_published',
            'created_at', 'updated_at', #'vaccines', #'is_vaccinated',
        ]
        
   # is_vaccinated = serializers.BooleanField(
   #     source='is_vaccinated',
   #     read_only=True,
   # )

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
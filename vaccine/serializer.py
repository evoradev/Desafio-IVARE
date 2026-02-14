from rest_framework import serializers
from .models import Vaccine

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = [
            'id', 'name', 'manufacturer', 'disease_prevented', 'public',
            'created_at', 'updated_at',
        ]

    public = serializers.BooleanField(
        source='is_published',
        read_only=True,
    )

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    updated_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

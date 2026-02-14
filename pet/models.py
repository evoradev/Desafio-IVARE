from django.contrib.auth.models import User
from django.db import models

class Pet(models.Model):

    class PetType(models.TextChoices):
        
        # Comuns - Específicos
        DOG = "DOG", "Dog"
        CAT = "CAT", "Cat"
        BIRD = "BIRD", "Bird"
        HORSE = "HORSE", "Horse"
        COW = "COW", "Cow"
        GOAT = "GOAT", "Goat"
        SHEEP = "SHEEP", "Sheep"
        PIG = "PIG", "Pig"

        # Genéricos
        FARM_ANIMAL = "FARM_ANIMAL", "Farm Animal"
        HOUSE_ANIMAL = "HOUSE_ANIMAL", "House Animal"
        AQUATIC_ANIMAL = "AQUATIC_ANIMAL", "Aquatic Animal"
        EXOTIC = "EXOTIC", "Exotic"

    name = models.CharField(max_length=50)

    owner = models.CharField(max_length=35)

    pet_type = models.CharField(
        max_length=30,
        choices=PetType.choices
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    #vaccines = models.ManyToManyField(
    #    "vaccines.Vaccine",
    #    blank=True,
    #    related_name="pets"
    #)

    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #@property
   # def is_vaccinated(self):
    #    return self.vaccines.exists()

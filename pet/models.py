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

    # Relacionamento com o usuário (dono do pet)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pets"
    )

    pet_type = models.CharField(
        max_length=30,
        choices=PetType.choices
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    vaccines = models.ManyToManyField(
        'vaccine.Vaccine',
        through='PetVaccination',
        related_name='pets',
        blank=True
    )


    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_vaccinated(self):
        return self.vaccines.exists()

class PetVaccination(models.Model):
    pet = models.ForeignKey(
        'pet.Pet',   
        on_delete=models.CASCADE,
        related_name='vaccinations'
    )

    vaccine = models.ForeignKey(
        'vaccine.Vaccine',
        on_delete=models.PROTECT,
        related_name='applications'
    )

    application_date = models.DateField(auto_now_add=True)
    number_of_aplications = models.PositiveIntegerField(default=1)
    batch_number = models.CharField(max_length=50, blank=True)
    veterinarian_name = models.CharField(max_length=150, blank=True)
    observations = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pet', 'vaccine', 'application_date')
        ordering = ['-application_date']

    def __str__(self):
        return f"{self.pet.name} - {self.vaccine.name}"
    
    

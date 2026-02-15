import factory
from faker import Faker
from django.contrib.auth.models import User

from pet.models import Pet, PetVaccination
from vaccine.models import Vaccine

fake = Faker("pt_BR")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyFunction(fake.user_name)
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)
    email = factory.LazyFunction(fake.email)

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "Senha@123"
        self.set_password(password)


class PetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pet

    user = factory.SubFactory(UserFactory)
    name = factory.LazyFunction(fake.first_name)

    owner_name = factory.LazyAttribute(lambda o: f"{o.user.first_name} {o.user.last_name}".strip() or o.user.username)

    pet_type = Pet.PetType.DOG

    description = factory.LazyFunction(lambda: fake.sentence(nb_words=10))

    is_published = True

    @factory.post_generation
    def vaccines(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for v in extracted:
                PetVaccination.objects.create(pet=self, vaccine=v)


class VaccineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vaccine

    name = factory.LazyFunction(lambda: f"Vacina {fake.word()}".title())
    manufacturer = factory.LazyFunction(fake.company)
    disease_prevented = factory.LazyFunction(lambda: fake.word().title())
    is_published = True


class PetVaccinationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PetVaccination

    pet = factory.SubFactory(PetFactory)
    vaccine = factory.SubFactory(VaccineFactory)

    number_of_aplications = 1
    batch_number = factory.LazyFunction(lambda: fake.bothify(text="LOT-#######"))
    veterinarian_name = factory.LazyFunction(fake.name)
    observations = factory.LazyFunction(lambda: fake.sentence(nb_words=12))

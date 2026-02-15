import factory
from faker import Faker
from vaccine.models import Vaccine

fake = Faker("pt_BR")


class VaccineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vaccine

    name = factory.LazyFunction(lambda: f"Vacina {fake.word()}".title())
    manufacturer = factory.LazyFunction(fake.company)
    disease_prevented = factory.LazyFunction(lambda: fake.word().title())
    is_published = True

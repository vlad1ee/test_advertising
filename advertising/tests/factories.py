import uuid
from django.contrib.auth import get_user_model

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from factory import SubFactory, PostGenerationMethodCall
from factory.faker import Faker
from advertising.models import Advertising, Category
from advertising.constants import ADVERTISING_STATUS_CHOICES


ADVERTISING_STATUS = [item[0] for item in ADVERTISING_STATUS_CHOICES]


class UserFactory(DjangoModelFactory):
    email = Faker('email')
    username = Faker('user_name')
    password = PostGenerationMethodCall('set_password', 'adminadmin123')
    is_superuser = True
    is_staff = True
    is_active = True

    class Meta:
        model = get_user_model()


class CategoryFactory(DjangoModelFactory):
    title = Faker('text', max_nb_chars=64)
    slug = Faker('text', max_nb_chars=255)

    class Meta:
        model = Category


class AdvertisingFactory(DjangoModelFactory):
    id = Faker('uuid4')
    title = Faker('text', max_nb_chars=64)
    description = Faker('text', max_nb_chars=255)
    category = SubFactory(CategoryFactory)
    status = FuzzyChoice(ADVERTISING_STATUS)
    author = SubFactory(UserFactory)

    class Meta:
        model = Advertising

from django.contrib.auth import get_user_model
from factory import fuzzy
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = fuzzy.FuzzyText()

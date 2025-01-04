import factory
from django.db.models.signals import post_save

from user.models.user import User


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user-{n}@example.com")
    password = factory.Sequence(lambda n: f"user-{n}")
    phone = "09123456789"

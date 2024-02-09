from django.db import transaction
from .models import User, Profile


def create_profile(*, user: User, first_name: str, last_name: str, age: int, gender: str) -> Profile:
    return Profile.objects.create(user=user, first_name=first_name, last_name=last_name, age=age, gender=gender)


def create_user(*, phone_number: str, password: str) -> User:
    return User.objects.create_user(phone_number=phone_number, password=password)


@transaction.atomic
def register(*, phone_number: str, password: str, first_name: str, last_name: str, age: int, gender: str, ) -> User:
    user = create_user(phone_number=phone_number, password=password)
    create_profile(user=user, first_name=first_name, last_name=last_name, age=age, gender=gender)
    return user

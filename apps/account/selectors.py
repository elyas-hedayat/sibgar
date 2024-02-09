from django.contrib.auth import get_user_model
from .models import Profile

user = get_user_model()


def get_profile(_user: user) -> Profile:
    return Profile.objects.get(user=_user)


def profile_list() -> Profile:
    return Profile.objects.all()

from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_staff


class Profile(models.Model):
    class GENDER(models.TextChoices):
        MALE = "مرد", "Male"
        FEMALE = "زن", "Female"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    gender = models.CharField(max_length=10, choices=GENDER.choices, )
    starting_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.first_name + self.last_name

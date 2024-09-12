from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, Model, ForeignKey, CASCADE, TextField, ImageField, TextChoices

from apps.models.base import SlugBaseModel
from apps.models.managers import CustomUserManager


class User(AbstractUser):
    class Type(TextChoices):
        OPERATOR = 'operator', 'Operator'
        MANAGER = 'manager', 'Manager'
        ADMIN = 'admin_side', 'Admin_side'
        DRIVER = 'currier', "Currier"
        USER = 'user', 'User'

    email = None
    username = None
    phone = CharField(max_length=12, unique=True)
    about = TextField(null=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)
    telegram_id = CharField(max_length=255, unique=True, null=True, blank=True)
    image = ImageField(upload_to='users/', null=True, blank=True)
    district = ForeignKey('apps.District', CASCADE, null=True, blank=True)
    type = CharField(max_length=25, choices=Type.choices, default=Type.USER)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []


class Region(Model):
    name = CharField(max_length=255)


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('apps.Region', CASCADE)

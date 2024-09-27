from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, Model, ForeignKey, CASCADE, TextField, ImageField, TextChoices, \
    PositiveIntegerField

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
    phone = CharField(verbose_name='Telefon Raqam', max_length=12, unique=True)
    about = TextField(verbose_name="User Haqida", null=True, blank=True)
    address = CharField(verbose_name="Manzil", max_length=255, null=True, blank=True)
    telegram_id = CharField(verbose_name="Telegram Id", max_length=255, unique=True, null=True, blank=True)
    image = ImageField(verbose_name="Rasmi", upload_to='users/', null=True, blank=True)
    district = ForeignKey('apps.District', CASCADE, verbose_name="Tuman", null=True, blank=True)
    type = CharField(verbose_name="Foydalanuvchi Turi", max_length=25, choices=Type.choices, default=Type.USER)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []


class Region(Model):
    name = CharField(verbose_name="Viloyat Nomi", max_length=255)


class District(Model):
    name = CharField(verbose_name="Tuman Nomi", max_length=255)
    region = ForeignKey('apps.Region', CASCADE, verbose_name="Viloyat")


class SiteSettings(Model):
    delivery_price_regions = PositiveIntegerField(verbose_name="Viloyatlar Uchun Yetkazib Berish Narxi", db_default=0)
    delivery_price_tashkent_region = PositiveIntegerField(verbose_name="Toshkent Viloyati Uchun Yetkazib Berish Narxi",
                                                          db_default=0)
    delivery_price_tashkent = PositiveIntegerField(verbose_name="Toshkent shahri Uchun Yetkazib Berish Narxi",
                                                   db_default=0)

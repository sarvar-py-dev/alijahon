from django.db.models import Model, ImageField, PositiveIntegerField, PositiveSmallIntegerField, CASCADE, \
    ForeignKey, BooleanField, TextField, CharField, TextChoices, SET_NULL
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import SlugBaseModel, TimeBaseModel


class Category(SlugBaseModel):
    image = ImageField(upload_to='categories/%Y/%m/%d')


class Product(SlugBaseModel, TimeBaseModel):
    description = CKEditor5Field()
    image = ImageField(upload_to='products/%Y/%m/%d')
    price = PositiveIntegerField()
    quantity = PositiveSmallIntegerField()
    category = ForeignKey('apps.Category', CASCADE, related_name='products')

    class Meta:
        ordering = '-created_at',


class Favourite(Model):
    user = ForeignKey('apps.User', CASCADE)
    product = ForeignKey('apps.Product', CASCADE)


class Order(TimeBaseModel):
    class StatusType(TextChoices):
        NEW = 'new', 'New'
        READY = "ready", 'Ready'
        DELIVER = "deliver", 'Deliver'
        DELIVERED = "delivered", 'Delivered'
        CANT_PHONE = "cant_phone", 'Cant_phone'
        CANCELED = "canceled", 'Canceled'
        ARCHIVED = "archived", 'Archived'

    product = ForeignKey('apps.Product', CASCADE)
    phone = CharField(max_length=12, unique=True)
    full_name = CharField(max_length=255)
    owner = ForeignKey('apps.User', SET_NULL, related_name='orders', null=True, blank=True)
    status = CharField(max_length=255, choices=StatusType.choices)
    region = ForeignKey('apps.Region', CASCADE)
    district = ForeignKey('apps.District', CASCADE)


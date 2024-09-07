from django.db.models import Model, ImageField, PositiveIntegerField, PositiveSmallIntegerField, CASCADE, \
    ForeignKey, BooleanField, TextField
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import SlugBaseModel, CreatedBaseModel


class Category(SlugBaseModel):
    image = ImageField(upload_to='categories/Y/m/d')


class Product(SlugBaseModel, CreatedBaseModel):
    description = CKEditor5Field()
    image = ImageField(upload_to='products/')
    price = PositiveIntegerField()
    quantity = PositiveSmallIntegerField()
    category = ForeignKey('apps.Category', CASCADE, 'category')


class Favourite(Model):
    user = ForeignKey('apps.User', CASCADE)
    product = ForeignKey('apps.Product', CASCADE)

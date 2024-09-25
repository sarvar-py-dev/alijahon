from django.db.models import Model, ImageField, PositiveIntegerField, PositiveSmallIntegerField, CASCADE, \
    ForeignKey, CharField, TextChoices, SET_NULL, IntegerField
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
    payment_referral = PositiveIntegerField(help_text="so'mda", null=True, blank=True)

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

    quantity = PositiveSmallIntegerField(db_default=1)
    product = ForeignKey('apps.Product', CASCADE)
    phone = CharField(max_length=12)
    full_name = CharField(max_length=255)
    owner = ForeignKey('apps.User', SET_NULL, related_name='orders', null=True, blank=True)
    status = CharField(max_length=255, choices=StatusType.choices, default=StatusType.NEW)
    region = ForeignKey('apps.Region', CASCADE, null=True, blank=True)
    district = ForeignKey('apps.District', CASCADE, null=True, blank=True)
    stream = ForeignKey('apps.Stream', SET_NULL, null=True, blank=True)

    @property
    def price(self):
        if self.stream:
            new_price = self.product.price - self.stream.discount
        else:
            new_price = self.product.price
        return new_price


class Stream(TimeBaseModel):
    name = CharField(max_length=255)
    discount = IntegerField(db_default=0)
    owner = ForeignKey('apps.User', CASCADE)
    product = ForeignKey('apps.Product', CASCADE)

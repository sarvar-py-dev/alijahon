from django.db.models import Model, ImageField, PositiveIntegerField, PositiveSmallIntegerField, CASCADE, \
    ForeignKey, CharField, TextChoices, SET_NULL, IntegerField, DateField
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import SlugBaseModel, TimeBaseModel


class Category(SlugBaseModel):
    image = ImageField(upload_to='categories/%Y/%m/%d')


class Product(SlugBaseModel, TimeBaseModel):
    description = CKEditor5Field(verbose_name="Mahsulot Haqida")
    image = ImageField(verbose_name="Mahsulot Rasmi", upload_to='products/%Y/%m/%d')
    price = PositiveIntegerField(verbose_name="Mahsulot Narxi")
    quantity = PositiveSmallIntegerField(verbose_name="Mahsulot Soni")
    category = ForeignKey('apps.Category', CASCADE, verbose_name="Mahsulot Categoriasi", related_name='products')
    payment_referral = PositiveIntegerField(verbose_name="Oqim Egasiga Beriladigan Pul", help_text="so'mda", default=0,
                                            null=True,
                                            blank=True)

    class Meta:
        ordering = '-created_at',


class Favourite(Model):
    user = ForeignKey('apps.User', CASCADE, verbose_name="Foydalanuvchi", related_name='favourites')
    product = ForeignKey('apps.Product', CASCADE, verbose_name="Mahsulot", related_name='favourites')


class Order(TimeBaseModel):
    class StatusType(TextChoices):
        NEW = 'new', 'New'
        READY = "ready", 'Ready'
        DELIVER = "deliver", 'Deliver'
        DELIVERED = "delivered", 'Delivered'
        CANT_PHONE = "cant_phone", 'Cant_phone'
        CANCELED = "canceled", 'Canceled'
        RETURNED = "returned", 'Returned'
        ARCHIVED = "archived", 'Archived'
        HOLD = "hold", 'Hold'

    quantity = PositiveSmallIntegerField(verbose_name="Buyurtma Soni", db_default=1)
    product = ForeignKey('apps.Product', CASCADE, verbose_name="Buyurtmaga Tegishli Mahsulot")
    phone = CharField(verbose_name="Buyurtma Beruvchining Telefon Raqami", max_length=12)
    full_name = CharField(verbose_name="Buyurtma Qabul Qiluvchi", max_length=255)
    owner = ForeignKey('apps.User', SET_NULL, verbose_name="Buyurtma Beruvchi", related_name='orders', null=True,
                       blank=True)
    status = CharField(verbose_name="Buyurtma Holati", max_length=255, choices=StatusType.choices,
                       default=StatusType.NEW)
    region = ForeignKey('apps.Region', CASCADE, verbose_name="Buyurtma Yetkaziladigan Viloyat", null=True, blank=True)
    district = ForeignKey('apps.District', CASCADE, verbose_name="Buyurtma Yetkaziladigan Tuman", null=True, blank=True)
    stream = ForeignKey('apps.Stream', SET_NULL, verbose_name="Buyurtma Oqimi", null=True, blank=True,
                        related_name='orders')

    @property
    def price(self):
        if self.stream:
            new_price = self.product.price - self.stream.discount
        else:
            new_price = self.product.price
        return new_price


class Stream(TimeBaseModel):
    name = CharField(verbose_name="Oqim Nomi", max_length=255)
    discount = IntegerField(verbose_name="Oqimning Chegirma Narhi", db_default=0)
    owner = ForeignKey('apps.User', CASCADE, verbose_name="Oqim Egasi")
    product = ForeignKey('apps.Product', CASCADE, verbose_name="Oqimning Mahsuloti")
    visit_count = PositiveIntegerField(verbose_name='Tashriflar Soni', default=0)


class Competition(TimeBaseModel):
    started_at = DateField(verbose_name='Konkurs Boshlanish Vaqti')
    ended_at = DateField(verbose_name='Konkurs Yakunlanish Vaqti')
    image = ImageField(verbose_name='Konkurs Uchun Rasm', upload_to='competition/')
    description = CKEditor5Field(verbose_name='Konkurs Uchun Tavsif')

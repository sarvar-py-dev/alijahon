from apps.models.users import User
from apps.models.shop import Product, Category, Order, Favourite


class ProductProxy(Product):
    class Meta:
        proxy = True
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'


class CategoryProxy(Category):
    class Meta:
        proxy = True
        verbose_name = 'Categoriya'
        verbose_name_plural = 'Categoriyalar'


class OrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'


# class NewOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = 'Yangi Buyurtma'
#         verbose_name_plural = 'Yangi'
#
#
# class ReadyOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = 'Dastavkaga tayyor Buyurtma'
#         verbose_name_plural = 'Dastavkaga tayyor'
#
#
# class DeliverOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = 'Yetkazilayotgan Buyurtma'
#         verbose_name_plural = 'Yetkazilmoqda'
#
#
# class DeliveredOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = 'Yetkazilgan Buyurtma'
#         verbose_name_plural = 'Yetkazildi'
#
#
# class CantPhoneOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = 'Bekor qilingan Buyurtma'
#         verbose_name_plural = 'Bekor qilindi'
#
#
# class CanceledOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = 'Qaytib kelgan Buyurtma'
#         verbose_name_plural = 'Qaytib keldi'


# class OrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = 'Yangi Buyurtma'
#         verbose_name_plural = 'Yangi'


# class ArchivedOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = 'Arhivlangan Buyurtma'
#         verbose_name_plural = 'Arhivlandi'


# class NewOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = 'Yangi Buyurtma'
#         verbose_name_plural = 'Yangi'


class UserProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class DriverUserProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Kuryer'
        verbose_name_plural = 'Kuryerlar'


class ManagerUserProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Manager'
        verbose_name_plural = 'Managerlar'


class OperatorUserProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Operator'
        verbose_name_plural = 'Operatorlar'


class FavouritesProxy(Favourite):
    class Meta:
        proxy = True
        verbose_name = 'Layk'
        verbose_name_plural = 'Layklar'

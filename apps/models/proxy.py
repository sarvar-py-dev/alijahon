from apps.models.proxy_manager import DriverUserManager, ManagerUserManager, OperatorUserManager, \
    AdminUserManager, UserUserManager
from apps.models.shop import Product, Category, Order, Favourite
from apps.models.users import User


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


class NewOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = 'Yangi Buyurtma'
        verbose_name_plural = 'Yangi'


class ReadyOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = 'Dastavkaga tayyor Buyurtma'
        verbose_name_plural = 'Dastavkaga tayyor'


class DeliverOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = 'Yetkazilayotgan Buyurtma'
        verbose_name_plural = 'Yetkazilmoqda'


class DeliveredOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = 'Yetkazilgan Buyurtma'
        verbose_name_plural = 'Yetkazildi'


class CantPhoneOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = 'Telefon Kutarmmadi'
        verbose_name_plural = 'Telefon kutarmadi'


class CanceledOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = 'Bekor qilingan Buyurtma'
        verbose_name_plural = 'Bekor qilindi'


class ReturnedOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = 'Qaytib keldi'
        verbose_name_plural = 'Qaytib keldi'


class ArchivedOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = 'Arhivlangan Buyurtma'
        verbose_name_plural = 'Arhivlandi'


class HoldOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = 'Hold'
        verbose_name_plural = 'Hold'


class UserProxy(User):
    objects = UserUserManager()

    class Meta:
        proxy = True
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class DriverUserProxy(User):
    objects = DriverUserManager()

    class Meta:
        proxy = True
        verbose_name = 'Kuryer'
        verbose_name_plural = 'Kuryerlar'


class ManagerUserProxy(User):
    objects = ManagerUserManager()

    class Meta:
        proxy = True
        verbose_name = 'Manager'
        verbose_name_plural = 'Managerlar'


class OperatorUserProxy(User):
    objects = OperatorUserManager()

    class Meta:
        proxy = True
        verbose_name = 'Operator'
        verbose_name_plural = 'Operatorlar'


class AdminUserProxy(User):
    objects = AdminUserManager()

    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Adminlar'


class FavouritesProxy(Favourite):
    class Meta:
        proxy = True
        verbose_name = 'Layk'
        verbose_name_plural = 'Layklar'

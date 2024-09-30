from django.contrib.admin import ModelAdmin, register, site
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from apps.models import ProductProxy, CategoryProxy
from apps.models.proxy import DriverUserProxy, OperatorUserProxy, ManagerUserProxy, UserProxy, AdminUserProxy, \
    OrderProxy, NewOrderProxy, ReadyOrderProxy, DeliverOrderProxy, DeliveredOrderProxy, CantPhoneOrderProxy, \
    CanceledOrderProxy, ReturnedOrderProxy, ArchivedOrderProxy, HoldOrderProxy

site.unregister(Group)


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("usable_password", "password1", "password2"),
            },
        ),
    )
    ordering = ['phone']
    list_display = ['phone']


@register(ProductProxy)
class ProductProxyModelAdmin(ModelAdmin):
    list_display = ("id", "name")


@register(CategoryProxy)
class CategoryModelAdmin(ModelAdmin):
    list_display = ("id", "name")


# def has_add_permission(self, request):
#     return False
#
# def has_delete_permission(self, request, obj=None):
#     return False

@register(DriverUserProxy)
class DriverUserProxyAdmin(CustomUserAdmin):
    pass


@register(OperatorUserProxy)
class OperatorUserProxyAdmin(CustomUserAdmin):
    pass


@register(ManagerUserProxy)
class ManagerUserProxyAdmin(CustomUserAdmin):
    pass


@register(UserProxy)
class UserProxyAdmin(CustomUserAdmin):
    pass


@register(AdminUserProxy)
class UserProxyAdmin(CustomUserAdmin):
    pass


@register(OrderProxy)
class OrderProxyAdmin(ModelAdmin):
    pass


@register(NewOrderProxy)
class NewOrderProxyAdmin(ModelAdmin):
    pass


@register(ReadyOrderProxy)
class ReadyOrderProxyAdmin(ModelAdmin):
    pass


@register(DeliverOrderProxy)
class DeliverOrderProxyAdmin(ModelAdmin):
    pass


@register(CantPhoneOrderProxy)
class CantPhoneOrderProxyAdmin(ModelAdmin):
    pass


@register(CanceledOrderProxy)
class CanceledOrderProxyAdmin(ModelAdmin):
    pass


@register(ReturnedOrderProxy)
class ReturnedOrderProxyAdmin(ModelAdmin):
    pass


@register(ArchivedOrderProxy)
class ArchivedOrderProxyAdmin(ModelAdmin):
    pass


@register(HoldOrderProxy)
class HoldOrderProxyAdmin(ModelAdmin):
    pass

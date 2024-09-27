from django.contrib.admin import ModelAdmin, register, site
from django.contrib.auth.models import Group

from apps.models import Category, ProductProxy, CategoryProxy

site.unregister(Group)


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

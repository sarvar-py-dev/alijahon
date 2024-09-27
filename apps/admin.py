from django.contrib.admin import ModelAdmin, register, site
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from apps.models import Product, Category

site.unregister(Group)


@register(Category)
class CategoryModelAdmin(ModelAdmin):
    pass

@register(Product)
class ProductModelAdmin(ModelAdmin):
    pass
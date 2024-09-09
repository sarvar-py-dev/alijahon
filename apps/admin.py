from django.contrib.admin import ModelAdmin, register

from apps.models import Product, Category


@register(Category)
class CategoryModelAdmin(ModelAdmin):
    pass

@register(Product)
class ProductModelAdmin(ModelAdmin):
    pass

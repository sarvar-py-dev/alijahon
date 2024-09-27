from apps.models import Product


class ProductModelProxy(Product):
    class Meta:
        proxy = True
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

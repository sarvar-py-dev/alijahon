from django.urls import path

from apps.views import ProductDetailView, ProductListView, CustomLoginView

urlpatterns = [
    path('', ProductListView.as_view(), name='list_view'),
    path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('login/', CustomLoginView.as_view(), name='login_page')
]

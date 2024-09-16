from django.urls import path

from apps.forms import ChangePasswordModelForm
from apps.views import ProductDetailView, ProductListView, CustomLoginView, CategoryListView, CategoryObjectListView, \
    ProfileDetailView, ProfileUpdateView, LogoutView, DistrictListView, OrderDetailView, OrderCreateView, \
    StreamListView, StreamProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', CategoryObjectListView.as_view(), name='category_object_list'),
    path('login/', CustomLoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout_page'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/settings/', ProfileUpdateView.as_view(
        fields=('image', 'first_name', 'last_name', 'address', 'telegram_id', 'district', 'about')),
         name='profile_settings'),
    path('profile/update-password/', ProfileUpdateView.as_view(
        form_class=ChangePasswordModelForm
    ), name='update_password'),
    path('get-districts/', DistrictListView.as_view(), name='get_districts'),
    path('success-product/<int:pk>/', OrderDetailView.as_view(), name='success_product'),
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('admin_page/urls/', StreamListView.as_view(), name='stream_list'),
    path('oqim/<int:pk>', StreamProductDetailView.as_view(), name='stream_product')
]

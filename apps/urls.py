from django.urls import path

from apps.forms import ChangePasswordModelForm
from apps.views import ProductDetailCreateView, ProductListView, CustomLoginView, CategoryListView, CategoryObjectListView, \
    ProfileDetailView, ProfileUpdateView, LogoutView, DistrictListView, OrderDetailView, StreamListView, \
    StreamProductDetailView, MarketListView, OrderListView, ProductStatisticDetailView, StreamCreateView, \
    StreamStatusListView

urlpatterns = [
    # Products
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', ProductDetailCreateView.as_view(), name='product_detail'),

    # Categories
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', CategoryObjectListView.as_view(), name='category_object_list'),

    # Orders
    path('success-product/<int:pk>/', OrderDetailView.as_view(), name='success_product'),
    path('profile/ordered-products', OrderListView.as_view(), name='order_list'),

    # Profile
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/settings/', ProfileUpdateView.as_view(
        fields=('image', 'first_name', 'last_name', 'address', 'telegram_id', 'district', 'about')),
         name='profile_settings'),
    path('profile/update-password/', ProfileUpdateView.as_view(
        form_class=ChangePasswordModelForm
    ), name='update_password'),
    path('get-districts/', DistrictListView.as_view(), name='get_districts'),

    # Login, Logout
    path('login/', CustomLoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout_page'),

    # Admin page
    path('admin-page/market/', MarketListView.as_view(), name='market'),
    path('admin-page/product/<int:pk>/', ProductStatisticDetailView.as_view(), name='statistic_product'),

    # Stream
    path('admin-page/urls/', StreamListView.as_view(), name='stream_list'),
    path('admin-page/stats/', StreamStatusListView.as_view(), name='stream_status'),
    path('oqim/<int:pk>', StreamProductDetailView.as_view(), name='stream_product'),
    path('oqim/create', StreamCreateView.as_view(), name='create_stream'),
]

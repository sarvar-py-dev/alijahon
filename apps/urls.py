from django.urls import path

from apps.forms import ChangePasswordModelForm
from apps.views import ProductDetailView, ProductListView, CustomLoginView, CategoryListView, CategoryObjectListView, \
    ProfileDetailView, ProfileUpdateView, LogoutView, DistrictListView

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

]

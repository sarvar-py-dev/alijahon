from django.urls import path

from apps.views import ProductDetailView, ProductListView, CustomLoginView, CategoryListView, CategoryObjectListView, \
    ProfileDetailView, ProfileUpdateView, LogoutView, PasswordUpdateView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', CategoryObjectListView.as_view(), name='category_object_list'),
    path('login/', CustomLoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout_page'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/settings/', ProfileUpdateView.as_view(), name='profile_settings'),
    path('profile/update-password/', PasswordUpdateView.as_view(), name='update_password')
]

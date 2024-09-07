from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from apps.forms import CustomAuthenticationForm
from apps.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'apps/product/product-list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/product/product-details.html'
    context_object_name = 'product'


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'apps/auth/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('list_view')

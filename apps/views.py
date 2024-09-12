from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.termcolors import RESET
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from typing_extensions import reveal_type

from apps.forms import CustomAuthenticationForm, ChangePasswordModelForm
from apps.models import Product, Category, User
from apps.models.user import Region


class ProductListView(ListView):
    model = Product
    template_name = 'apps/product/product-list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/product/product-details.html'
    context_object_name = 'product'


class CategoryListView(ListView):
    model = Category
    template_name = 'apps/product/category-list.html'
    context_object_name = 'categories'
    paginate_by = 13

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['products'] = Product.objects.all()
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        if search := self.request.GET.get('search'):
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return qs


class CategoryObjectListView(ListView):
    model = Category
    template_name = 'apps/product/category-list.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['products'] = Product.objects.filter(category__slug=ctx['view'].kwargs.get('slug'))

        return ctx


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'apps/auth/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('product_list')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('product_list'))


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'apps/auth/profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'apps/auth/profile-settings.html'
    fields = 'image', 'first_name', 'last_name', 'address', 'telegram_id', 'district', 'about'
    success_url = reverse_lazy('profile_settings')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['regions'] = Region.objects.all()
        return ctx


class PasswordUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'apps/auth/profile-settings.html'
    form_class = ChangePasswordModelForm
    success_url = reverse_lazy('profile_settings')

    def get_object(self, queryset=None):
        return self.request.user

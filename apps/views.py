from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from apps.forms import CustomAuthenticationForm
from apps.models import Product, Category, User, Region, District


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
    model = Product
    template_name = 'apps/product/category-list.html'
    context_object_name = 'products'
    paginate_by = 13

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        if search := self.request.GET.get('search'):
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return qs


class CategoryObjectListView(ListView):
    model = Product
    template_name = 'apps/product/category-list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        if slug := self.kwargs.get('slug'):
            qs.filter(category__slug=slug)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = Category.objects.all()
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
    success_url = reverse_lazy('profile_settings')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['regions'] = Region.objects.all()
        ctx['districts'] = District.objects.all()
        return ctx


class DistrictListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        region_id = request.GET.get('region_id')
        if region_id:
            districts = District.objects.filter(region_id=region_id).values('id', 'name')
            return JsonResponse(list(districts), safe=False)
        return JsonResponse([], safe=False)


class OrderCreateView(CreateView):
    pass

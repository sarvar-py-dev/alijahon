from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from apps.forms import CustomAuthenticationForm, OrderCreateModelForm, StreamCreateModelForm
from apps.models import Product, Category, User, Region, District, Order, Stream, SiteSettings


class ProductListView(ListView):
    model = Product
    template_name = 'apps/product/product-list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class ProductDetailView(DetailView, CreateView):
    model = Product
    template_name = 'apps/product/product-detail.html'
    form_class = OrderCreateModelForm
    context_object_name = 'product'

    def form_valid(self, form):
        order = form.save()
        if len(form.cleaned_data['phone']) != 12:
            raise ValidationError('number must be 12 in length')
        return redirect('success_product', pk=order.pk)


class ProductStatisticDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'apps/product/product-statistics.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['all_stream_len'] = Stream.objects.count()
        ctx['user_stream_len'] = Stream.objects.filter(owner=self.request.user).count()

        return ctx


class CategoryListView(ListView):
    model = Product
    template_name = 'apps/product/category-list.html'
    context_object_name = 'products'
    paginate_by = 10

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


class OrderDetailView(DetailView):
    model = Order
    template_name = 'apps/order/success-product.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['delivery'] = SiteSettings.objects.first()
        return ctx


class OrderListView(ListView):
    model = Order
    template_name = 'apps/order/order-list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = super().get_queryset().filter(phone=self.request.user.phone)
        return qs

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_page')
        return super().get(request, *args, **kwargs)


class MarketListView(ProductListView):
    template_name = 'apps/stream/market.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if category_slug := self.request.GET.get('category'):
            qs = qs.filter(category__slug=category_slug)
        return qs


class StreamListView(ListView):
    model = Stream
    template_name = 'apps/stream/stream.html'
    context_object_name = 'streams'


class StreamProductDetailView(DetailView):
    model = Stream
    template_name = 'apps/product/product-detail.html'


class StreamCreateView(CreateView):
    model = Product
    template_name = 'apps/stream/market.html'
    context_object_name = 'products'
    form_class = StreamCreateModelForm
    success_url = reverse_lazy('stream_list')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)




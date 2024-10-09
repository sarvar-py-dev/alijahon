from datetime import timedelta

from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.db.models import Q, Count, F, Sum
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView

from apps.forms import CustomAuthenticationForm, OrderCreateModelForm, StreamCreateModelForm
from apps.models import Product, Category, User, Region, District, Order, Stream, SiteSettings, Favourite, Competition


class ProductListView(ListView):
    model = Product
    template_name = 'apps/product/product-list.html'
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


class StreamProductDetailCreateView(DetailView, CreateView):
    model = Product
    template_name = 'apps/product/product-detail.html'
    form_class = OrderCreateModelForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if stream_pk := self.kwargs.get('pk'):
            ctx['stream'] = Stream.objects.filter(pk=stream_pk).first()
            ctx['product'] = ctx['stream'].product
            ctx['stream'].visit_count += 1
            ctx['stream'].save()
        return ctx

    def form_valid(self, form):
        order = form.save()
        if len(form.cleaned_data['phone']) != 9:
            raise ValidationError('number must be 12 in length')
        return redirect('success_product', pk=order.pk)


class ProductStatisticDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'apps/product/product-statistics.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        streams = Stream.objects.filter(product=ctx['product'])
        ctx['all_stream_len'] = streams.count()
        ctx['user_stream_len'] = streams.filter(owner=self.request.user).count()

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

    def form_invalid(self, form):
        return super().form_invalid(form)


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
        if region_id := request.GET.get('region_id'):
            districts = District.objects.filter(region_id=region_id).values('id', 'name')
            return JsonResponse(list(districts), safe=False)
        return JsonResponse([], safe=False)


class OrderDetailView(DetailView):
    queryset = Order.objects.all()
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
    template_name = 'apps/admin-page/market.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if search := self.request.GET.get('search'):
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if category_slug := self.request.GET.get('category'):
            if category_slug == 'top':
                qs = qs.annotate(order_count=Count('order')).filter(
                    order__status=Order.StatusType.DELIVERED).order_by('-order_count', '-order__quantity')
            else:
                qs = qs.filter(category__slug=category_slug)
        return qs


class StreamListView(ListView):
    model = Stream
    template_name = 'apps/admin-page/stream.html'
    context_object_name = 'streams'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs


class StreamCreateView(CreateView):
    model = Stream
    template_name = 'apps/admin-page/market.html'
    form_class = StreamCreateModelForm
    success_url = reverse_lazy('stream_list')

    def form_valid(self, form):
        stream = form.save(False)
        stream.owner = self.request.user
        stream.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class StreamStatusListView(ListView):
    model = Stream
    template_name = 'apps/admin-page/stats.html'
    context_object_name = 'streams'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)

        if period := self.request.GET.get('period'):
            if period == 'today':
                qs = qs.filter(orders__created_at__exact=now().date())
            elif period == 'last_day':
                qs = qs.filter(orders__created_at__exact=now().date() - timedelta(1))
            elif period == 'weekly':
                qs = qs.filter(orders__created_at__gte=now() - timedelta(now().weekday()))
            elif period == 'monthly':
                qs = qs.filter(orders__created_at__year=now().year, orders__created_at__month=now().month)

        qs = qs.annotate(
            new=Count('orders', Q(orders__status='new') & Q(orders__stream_id=F('id'))),
            ready=Count('orders', Q(orders__status='ready') & Q(orders__stream_id=F('id'))),
            deliver=Count('orders', Q(orders__status='deliver') & Q(orders__stream_id=F('id'))),
            delivered=Count('orders', Q(orders__status='delivered') & Q(orders__stream_id=F('id'))),
            cant_phone=Count('orders', Q(orders__status='cant_phone') & Q(orders__stream_id=F('id'))),
            canceled=Count('orders', Q(orders__status='canceled') & Q(orders__stream_id=F('id'))),
            archived=Count('orders', Q(orders__status='archived') & Q(orders__stream_id=F('id'))),
        )
        qs.aggregates = qs.aggregate(
            total_visit_count=Sum('visit_count'),
            total_new=Sum('new'),
            total_ready=Sum('ready'),
            total_deliver=Sum('deliver'),
            total_delivered=Sum('delivered'),
            total_cant_phone=Sum('cant_phone'),
            total_canceled=Sum('canceled'),
            total_archived=Sum('archived')
        )
        return qs


class AdminPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/admin-page/menu.html'


class FavouriteView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        obj, created = Favourite.objects.get_or_create(user=request.user, product_id=pk)
        if not created:
            obj.delete()
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)


class FavouriteListView(LoginRequiredMixin, ListView):
    model = Favourite
    template_name = 'apps/admin-page/favourite.html'
    context_object_name = 'favourites'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OrderStreamRequestListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'apps/admin-page/request.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(stream__owner=self.request.user)

        return qs


class PaymentTemplateView(TemplateView):
    template_name = 'apps/admin-page/payment.html'


class CompetitionListView(DetailView):
    model = Competition
    template_name = 'apps/admin-page/competition.html'

    def get_object(self, queryset=None):
        return '1'


class BrokenOrderOperatorTemplateView(TemplateView):
    template_name = 'apps/operator/operator-broken.html'


class DeliveringOrderOperatorTemplateView(TemplateView):
    template_name = 'apps/operator/operator-delivering.html'


class HoldOrderOperatorTemplateView(TemplateView):
    template_name = 'apps/operator/operator-hold.html'


class NewOrderOperatorTemplateView(TemplateView):
    template_name = 'apps/operator/operator-new.html'


class OrderOperatorTemplateView(TemplateView):
    template_name = 'apps/operator/operator-order-detail.html'


class AddOrderOperatorTemplateView(TemplateView):
    template_name = 'apps/operator/operator-product-add.html'


class ReadyOrderOperatorTemplateView(TemplateView):
    template_name = 'apps/operator/operator-ready.html'


class WaitingOrderOperatorTemplateView(TemplateView):
    template_name = 'apps/operator/operator-waiting.html'

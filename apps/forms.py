import re
from itertools import product

from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.forms import CharField, PasswordInput, ModelForm, Form, ModelChoiceField
from django.utils.translation import gettext_lazy as _

from apps.models import User, Order, Product


class CustomAuthenticationForm(Form):
    phone = CharField()
    password = CharField(
        label=_("Password"),
        strip=False,
        widget=PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(phone)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.data.get('phone')
        return re.sub(r'[^\d]', '', phone)

    def clean(self):
        phone = self.cleaned_data.get("phone")
        password = self.cleaned_data.get("password")

        if phone is not None and password:
            if not User.objects.filter(phone=phone).exists():
                self.user_cache = User.objects.create_user(phone=phone, password=password)
            else:
                self.user_cache = authenticate(
                    self.request, phone=phone, password=password
                )
            if self.user_cache is None:
                raise ValidationError(self.error_messages["inactive"],
                                      code="inactive")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache


class ChangePasswordModelForm(ModelForm):
    new_password1 = CharField(max_length=255)
    new_password2 = CharField(max_length=255)

    class Meta:
        model = User
        fields = 'password', 'new_password1', 'new_password2'

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.instance.check_password(password):
            raise ValidationError('Password xato')
        return password

    def clean(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise ValidationError('Password xato')

        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
        return user


class OrderCreateModelForm(ModelForm):
    # product = ModelChoiceField(Product.objects.all())
    phone = CharField(max_length=18)

    class Meta:
        model = Order
        exclude = 'quantity', 'status', 'region', 'district'

    def clean_phone(self):
        phone = self.data.get('phone')
        return re.sub(r'[^\d]', '', phone)

    def clean_product(self):
        return self.cleaned_data['product']

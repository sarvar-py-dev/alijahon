from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import CharField, PasswordInput, ModelForm, Form
from django.utils.translation import gettext_lazy as _
import re

from apps.models import User


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
                raise self.get_invalid_login_error()
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
    # old_password =
    # new_password1 =
    # new_password2 =
    pass

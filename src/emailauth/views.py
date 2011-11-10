from django.contrib.auth.views import login as default_login, password_reset as \
    default_password_reset
from emailauth.forms import AuthenticationForm, PasswordResetForm

def login(request, **kwargs):
    kwargs.setdefault('authentication_form', AuthenticationForm)
    return default_login(request, **kwargs)

def password_reset(request, **kwargs):
    kwargs.setdefault('password_reset_form', PasswordResetForm)
    return default_password_reset(request, **kwargs)

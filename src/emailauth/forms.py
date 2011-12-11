from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from emailauth import settings

class AuthenticationForm(forms.Form):
    email = forms.EmailField(label=_("E-mail address"), max_length=settings.MAXIMUM_EMAIL_LENGTH)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def authenticate(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct e-mail address and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        return self.user_cache

    def clean(self):
        self.authenticate()
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                _("Your Web browser doesn't appear to have cookies enabled. "
                "Cookies are required for logging in."))

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(label=_("E-mail address"), max_length=settings.MAXIMUM_EMAIL_LENGTH)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(_("A user with that e-mail address already exists."))
        except User.DoesNotExist:
            return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ("email",)

class UserChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    class Meta:
        model = User

class PasswordResetForm(BasePasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].max_length = settings.MAXIMUM_EMAIL_LENGTH

ADMIN_LOGIN_ERROR_MESSAGE = _("Please enter the correct e-mail address and password for a staff account.")

class AdminAuthenticationForm(AuthenticationForm):
    this_is_the_login_form = forms.BooleanField(widget=forms.HiddenInput, initial=1,
        error_messages={'required': _("Please log in again, because your session has expired.")})

    def clean(self):
        user = self.authenticate()
        if user is None or not user.is_staff:
            raise forms.ValidationError(ADMIN_LOGIN_ERROR_MESSAGE)
        self.check_for_test_cookie()
        return self.cleaned_data

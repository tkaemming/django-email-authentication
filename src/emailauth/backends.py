from django.contrib.auth.backends import ModelBackend as BaseModelBackend
from django.contrib.auth.models import User

class ModelBackend(BaseModelBackend):
    supports_anonymous_user = False

    def authenticate(self, email=None, password=None):
        if None in (email, password):
            return

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass

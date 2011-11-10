from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
from emailauth import settings

username_field = User._meta.get_field_by_name('username')[0]
username_field.max_length = settings.MAXIMUM_USERNAME_LENGTH

email_field = User._meta.get_field_by_name('email')[0]
email_field._unique = True
email_field.max_length = settings.MAXIMUM_EMAIL_LENGTH
email_field.blank = False
email_field.null = False

@receiver(pre_save, sender=User)
def mirror_username_to_email(sender, instance, *args, **kwargs):
    instance.username = instance.email

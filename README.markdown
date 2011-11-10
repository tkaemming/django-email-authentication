# django-email-authentication

An extension to `django.contrib.auth` that replaces username-based authentication
with email-based authentication, without requiring any changes to existing 
applications that depend on the `django.contrib.auth.User` model.

## Installation

* Add `emailauth` to your `INSTALLED_APPS` in your Django settings file.
* Replace `django.contrib.backends.ModelBackend` in the `AUTHENTICATION_BACKENDS`
  setting with `emailauth.backends.ModelBackend`. It's not recommended that you
  use both the built-in `ModelBackend` and the replacement `ModelBackend` at 
  the same time (although it it technically possible to do so.)
* Replace the following built-in forms and views:
    * `django.contrib.auth.views.login` with `emailauth.views.login`
    * `django.contrib.auth.views.password_reset` with `emailauth.views.password_reset`
    * `django.contrib.auth.forms.AuthenticationForm` with `emailauth.forms.AuthenticationForm`
    * `django.contrib.auth.forms.UserCreationForm` with `emailauth.forms.UserCreationForm`
    * `django.contrib.auth.forms.UserChangeForm` with `emailauth.forms.UserChangeForm`
    * `django.contrib.auth.forms.PasswordResetForm` with `emailauth.forms.PasswordResetForm`
    * `django.contrib.auth.forms.AdminAuthenticationForm` with `emailauth.forms.AdminAuthenticationForm`
* If you use a custom `AdminSite` instance, modify it to match the implementation
  in `emailauth.admin`.
* If you have modified the default `registration/password_reset_email.html` 
  template, update it to match the template provided with `emailauth`. (If you
  have not modified it, no action is necessary.)
* Make sure that you're not using `username` anywhere in your application.

## Important Caveats

This is not simply a drop-in application. This application [monkey patches][monkeypatch]
the buit-in `User` model in several ways that could break existing applications,
and will at least require a database migration on existing projects. These include:

* Changes to the `User` model:
    * The `username` field has `max_length=254`. (This is modifiable by 
        `settings.MAXIMUM_USERNAME_LENGTH`, which is the same as 
        `settings.MAXIMUM_EMAIL_LENGTH`, unless otherwise specified.)
    * The `email` field now has these changed attributes:
        * `blank=False`
        * `null=False`
        * `unique=True`
        * `max_length=254` (This is modifiable by `settings.MAXIMUM_EMAIL_LENGTH`)
* The addition a signal to ensure that `User.username` is a mirror of `User.email` 
  (This may interact in unexpected/catastrophic ways with existing data!)

## Disclaimer

This is basically one big hack on top of the built-in `auth` module to coerce it
into behaving in ways it was not designed to behave by using dirty hacks and 
abusing the private Model API. This is not guaranteed to continue to work with
any version of Django in the future (or any current or previous versions, for 
that matter.)

[monkeypatch]: http://en.wikipedia.org/wiki/Monkey_patch

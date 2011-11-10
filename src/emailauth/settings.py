from django.conf import settings

# corresponds to the default max_length of EmailField, unless otherwise specified
# a sane default for this field would be minimum of 254
# see: http://en.wikipedia.org/wiki/Email_address#Syntax
MAXIMUM_EMAIL_LENGTH = getattr(settings, 'MAXIMUM_EMAIL_LENGTH', 254)

# corresponds to the specified max_length of User.username, unless otherwise specified
# it's recommended that you tie this to the value of MAXIMUM_EMAIL_LENGTH
MAXIMUM_USERNAME_LENGTH = getattr(settings, 'MAXIMUM_USERNAME_LENGTH', MAXIMUM_EMAIL_LENGTH)

#
#   wayne_django_rest copyright © 2020 - all diricts reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.contrib import admin
from .models import SocialAccount, SocialAccountUsername, SocialAccountEmail

admin.site.register(SocialAccount)
admin.site.register(SocialAccountUsername)
admin.site.register(SocialAccountEmail)

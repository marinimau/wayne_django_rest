#
#   wayne_django_rest copyright © 2020 - all diricts reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.contrib import admin
from .models import SocialWall, SocialLabel, SocialAccount

admin.site.register(SocialWall)
admin.site.register(SocialLabel)
admin.site.register(SocialAccount)

from django.contrib import admin


from .models import SocialLabel, SocialAccount

admin.site.register(SocialLabel)
admin.site.register(SocialAccount)

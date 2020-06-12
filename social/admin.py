from django.contrib import admin

# Register your models here.
from .models import SocialLabel, SocialAccount

admin.site.register(SocialLabel)
admin.site.register(SocialAccount)

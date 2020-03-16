from django.contrib import admin

# Register your models here.
from user.models import Profile, ResetPasswordToken

admin.site.register(Profile)
admin.site.register(ResetPasswordToken)

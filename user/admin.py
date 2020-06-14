from django.contrib import admin
from user.models import Profile, ResetPasswordToken


admin.site.register(Profile)
admin.site.register(ResetPasswordToken)

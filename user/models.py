from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Profile(models.Model):

    class Gender(models.TextChoices):
        MALE = 'M', _('M')
        FEMALE = 'F', _('F')
        OTHER = 'O', _('O')
        UNSPECIFIED = 'U', _('U')

    class Country(models.TextChoices):
        IT = 'IT', _('Italy')
        US = 'US', _('United States')
        FR = 'FR', _('France')

    class Language(models.TextChoices):
        IT = 'IT', _('Italy')
        EN = 'EN', _('English')

    class UIMode(models.TextChoices):
        L = 'L', _('Light')
        D = 'D', _('Dark')
        A = 'A', _('Auto')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    cellular = models.TextField(null=True, max_length=40, blank=True)
    gender = models.CharField(null=False, max_length=1, choices=Gender.choices, default=Gender.UNSPECIFIED)
    country = models.CharField(null=False, max_length=2, choices=Country.choices, default=Country.IT)
    language = models.CharField(null=False, max_length=2, choices=Language.choices, default=Language.EN)
    ui_pref = models.CharField(null=False, max_length=1, choices=UIMode.choices, default=UIMode.A)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



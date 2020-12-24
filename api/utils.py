#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from api.user.tokens import account_activation_token
from django.conf import settings

site_url = settings.SITE_URL
sender = settings.EMAIL_HOST_USER


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_confirm_registration_email(user):
    send_mail(
        'Oudi - Activate Your Account',
        render_to_string('./email_templates/account_activation_email.html', {
            'user': user,
            'domain': site_url,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }),
        sender,
        [user.email_user],
        fail_silently=False,
    )


def send_reset_password_email(user, ip, user_agent, token):
    send_mail(
        subject='Oudi - Reset your password',
        message='prova',
        from_email=sender,
        recipient_list=[user.email_user],
        fail_silently=False,
    )


def send_reset_password__confirm_email(user):
    send_mail(
        'Oudi - Reset your password',
        render_to_string('./email_templates/password_modified_email.html', {
            'user': user,
            'domain': site_url
        }),
        sender,
        [user.email_user],
        fail_silently=False,
    )

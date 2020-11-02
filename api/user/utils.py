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

from api.user.tokens import account_activation_token


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_confirm_registration_email(user):
    subject = 'Wayne - Activate Your Account'
    message = render_to_string('./email_templates/account_activation_email.html', {
        'user': user,
        'domain': 'wayneighboors.com',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)


def send_reset_password_email(user, ip, user_agent, token):
    subject = 'Wayne - Reset your password'
    message = render_to_string('./email_templates/reset_password_email.html', {
        'user': user,
        'domain': 'wayneighboors.com',
        'ip': ip,
        'user_agent': user_agent,
        'token': token,
    })
    user.email_user(subject, message)


def send_reset_password__confirm_email(user):
    subject = 'Wayne - Reset your password'
    message = render_to_string('./email_templates/password_modified_email.html', {
        'user': user,
        'domain': 'wayneighboors.com'
    })
    user.email_user(subject, message)

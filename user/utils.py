from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from user.tokens import account_activation_token


def send_confirm_registration_email(user):
    subject = 'Wayne - Activate Your Account'
    message = render_to_string('email_templates/account_activation_email.html', {
        'user': user,
        'domain': 'wayneighboors.com',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)

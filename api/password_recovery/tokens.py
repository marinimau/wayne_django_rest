#
#   wayne_django_rest copyright © 2020 - all diricts reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

import secrets
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ResetPasswordTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return secrets.token_hex(6)


password_reset_token = ResetPasswordTokenGenerator()

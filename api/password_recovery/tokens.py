import secrets
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ResetPasswordTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return secrets.token_hex(6)


password_reset_token = ResetPasswordTokenGenerator()

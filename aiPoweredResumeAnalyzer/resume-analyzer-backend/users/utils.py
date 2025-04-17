from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.tokens import default_token_generator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

email_verification_token = EmailVerificationTokenGenerator()
# utils/email_verification_token.py


def make_token(user):
    return default_token_generator.make_token(user)

def check_token(user, token):
    return default_token_generator.check_token(user, token)

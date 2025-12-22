from django.core import signing
from django.conf import settings


class EmailVerificationToken:
    SALT = "email-verification"

    @staticmethod
    def make_token(user):
        return signing.dumps(
            {"user_id": user.pk},
            salt=EmailVerificationToken.SALT,
        )

    @staticmethod
    def verify_token(token, max_age=60 * 60 * 24):  # 24 hours
        try:
            data = signing.loads(
                token,
                salt=EmailVerificationToken.SALT,
                max_age=max_age,
            )
            return data["user_id"]
        except signing.BadSignature:
            return None

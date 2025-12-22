from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from .tokens import EmailVerificationToken


def send_verification_email(user, request):
    token = EmailVerificationToken.make_token(user)
    verify_url = request.build_absolute_uri(
        reverse("accounts:verify-email", args=[token])
    )

    send_mail(
        subject="Verify your email address",
        message=(
            f"Hi,\n\n"
            f"Please verify your email by clicking the link below:\n\n"
            f"{verify_url}\n\n"
            f"If you did not sign up, you can ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

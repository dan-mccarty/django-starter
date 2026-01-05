# accounts/emails.py
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def build_base_url(request) -> str:
    base = getattr(settings, "FRONTEND_BASE_URL", "").rstrip("/")
    if base:
        return base
    scheme = "https" if request.is_secure() else "http"
    return f"{scheme}://{request.get_host()}"


def send_verification_email(request, user) -> None:
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verify_path = reverse(
        "accounts:verify-email", kwargs={"uidb64": uidb64, "token": token}
    )
    verify_url = f"{build_base_url(request)}{verify_path}"

    subject = "Verify your email address"

    context = {"user": user, "verify_url": verify_url}
    text_body = render_to_string("emails/verify_email.txt", context)
    html_body = render_to_string("emails/verify_email.html", context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        to=[user.email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)

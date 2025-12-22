from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from django.views import View

from .models import User
from .tokens import EmailVerificationToken


class VerifyEmailView(View):
    def get(self, request, token):
        user_id = EmailVerificationToken.verify_token(token)

        if not user_id:
            return HttpResponseBadRequest("Invalid or expired verification link.")

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return HttpResponseBadRequest("User does not exist.")

        if not user.is_email_verified:
            user.is_email_verified = True
            user.save(update_fields=["is_email_verified"])

        return redirect("login")  # or a success page

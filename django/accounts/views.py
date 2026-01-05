# accounts/views.py
from django.shortcuts import redirect, render
from django.views.generic import FormView

from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth import get_user_model
from django.views import View
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from .forms import SignUpForm
from .emails import send_verification_email
from .models.account import Account
from django.contrib.auth.views import LoginView, LogoutView

User = get_user_model()


class SignUpView(FormView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = "/accounts/login/"

    def form_valid(self, form):
        user = form.save(commit=False)
        account = Account.objects.create(name=form.cleaned_data["email"])

        user.account = account

        user.is_active = False
        if hasattr(user, "is_email_verified"):
            user.is_email_verified = False
        user.save()

        send_verification_email(self.request, user)

        if self.request.headers.get("HX-Request") == "true":
            return render(
                self.request,
                "accounts/partials/signup_success.html",
                {"email": user.email},
            )

        return super().form_valid(form)


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (ValueError, TypeError, User.DoesNotExist):
            user = None

        success = user and default_token_generator.check_token(user, token)

        if success:
            updates = []
            if not user.is_active:
                user.is_active = True
                updates.append("is_active")
            if hasattr(user, "is_email_verified") and not user.is_email_verified:
                user.is_email_verified = True
                updates.append("is_email_verified")

            if updates:
                user.save(update_fields=updates)

            login(request, user)

        template = (
            "accounts/partials/verify_result.html"
            if request.headers.get("HX-Request") == "true"
            else "accounts/verify_result.html"
        )

        return render(request, template, {"success": bool(success)})


@method_decorator(require_http_methods(["GET", "POST"]), name="dispatch")
class ResendVerificationView(View):
    template_name = "accounts/resend_verification.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = (request.POST.get("email") or "").strip()
        user = User.objects.filter(email__iexact=email).first()

        if user and not user.is_active:
            send_verification_email(request, user)

        # Always same response (prevents user enumeration)
        if request.headers.get("HX-Request") == "true":
            return render(request, "accounts/partials/resend_done.html")

        return render(request, self.template_name, {"resent": True})

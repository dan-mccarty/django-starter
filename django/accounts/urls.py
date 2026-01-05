from django.urls import path

# from .views import AccountLoginView, AccountLogoutView, SignupView, VerifyEmailView
from .views import (
    SignUpView,
    VerifyEmailView,
    ResendVerificationView,
    LoginView,
    LogoutView,
)

app_name = "accounts"

urlpatterns = [
    # path("login/", AccountLoginView.as_view(), name="login"),
    # path("logout/", AccountLogoutView.as_view(), name="logout"),
    # path("signup/", SignupView.as_view(), name="signup"),
    # path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path(
        "login/", LoginView.as_view(template_name="accounts/login.html"), name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify-email"),
    path(
        "resend-verification/",
        ResendVerificationView.as_view(),
        name="resend-verification",
    ),
]

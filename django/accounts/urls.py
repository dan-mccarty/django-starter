from django.urls import path
from .views import VerifyEmailView

app_name = "accounts"

urlpatterns = [
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
]

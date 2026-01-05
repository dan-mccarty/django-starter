from django.shortcuts import redirect
from django.urls import path
from django.conf import settings


def home(request):
    return redirect(settings.LOGIN_URL)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.db.models import F, Q, Count
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


def landing_page(request):
    context = {}
    return render(request, "landing_page.html", context)


def recipes(request):
    context = {}
    return render(request, "recipes.html", context)


def sign_up(request):
    context = {}
    return render(request, "sign_up.html", context)


def login_page(request):
    context = {"login_form": LoginForm()}
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if "login_request" in request.POST:
            if not login_form.is_valid():
                print(login_form.errors)
                HttpResponseRedirect("#")
            elif login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('cooking_post:dashboard')
                else:
                    print("user is none or incorrect creds")
                    HttpResponseRedirect("#")
    else:
        login_form = LoginForm()
        return render(request, "login.html", context)

@login_required
def dashboard(request):
    context = {}
    return render(request, "dashboard.html", context)
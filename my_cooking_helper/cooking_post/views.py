from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.db.models import F, Q, Count
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

# Create your views here.
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
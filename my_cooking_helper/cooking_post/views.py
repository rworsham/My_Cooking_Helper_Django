import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm
from cooking_data.models import Recipe, Rating
from cooking_data.utils import get_highest_rated_recipes

def landing_page(request):
    context = {"featured_recipes": get_highest_rated_recipes(limit=3)}
    return render(request, "landing_page.html", context)


def recipes(request):
    context = {}
    return render(request, "recipes.html", context)

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    instructions = recipe.instructions.splitlines()
    existing_rating = Rating.objects.filter(user=request.user, recipe=recipe).first()
    if request.method == 'POST':
        score = request.POST.get('score')
        Rating.objects.update_or_create(
            user=request.user,
            recipe=recipe,
            defaults={'score': score}
        )
        return HttpResponseRedirect(request.path)

    context = {
        'recipe': recipe,
        'existing_rating': existing_rating,
        'instructions': instructions
    }

    return render(request, 'recipe_detail.html', context)

def featured_recipes(request):
    context = {"featured_recipes": get_highest_rated_recipes()}
    return render(request, "featured_recipes.html", context)

def search_recipes(request):
    query = request.GET.get('q')
    results = []
    if query and len(query) < 80:
        results = Recipe.objects.filter(name__icontains=query)
    return render(request, 'search_recipes.html', {'results': results, 'query': query})


def sign_up(request):
    context = {"sign_up_form": SignUpForm()}
    if request.method == "POST":
        sign_up_form = SignUpForm(request.POST)
        if "sign_up_form" in request.POST:
            if not sign_up_form.is_valid():
                print(sign_up_form.errors)
                HttpResponseRedirect("#")
            elif sign_up_form.is_valid():
                new_user = User(
                    username=sign_up_form.cleaned_data['email'],
                    first_name=sign_up_form.cleaned_data['name'],
                    email=sign_up_form.cleaned_data['email'],
                    password=make_password(sign_up_form.cleaned_data['password'])
                )
                new_user.save()
                HttpResponseRedirect('cooking_post:login_page')

    else:
        sign_up_form = SignUpForm()
        return render(request, "sign_up.html", context)


def login_page(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data["email"]
            password = login_form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('cooking_post:dashboard')
            else:
                print("Invalid email or password")
                return render(request, "login.html", {"login_form": login_form, "error": "Invalid credentials."})
        print(login_form.errors)
        return render(request, "login.html", {"login_form": login_form})
    else:
        login_form = LoginForm()
    return render(request, "login.html", {"login_form": login_form})


@login_required
def logout_user(request):
    logout(request)
    return redirect("cooking_post:landing_page")

def get_random_recipes(num_recipes=7):
    all_recipes = list(Recipe.objects.all())
    num_recipes = min(num_recipes, len(all_recipes))
    random_recipes = random.sample(all_recipes, num_recipes)
    return random_recipes


@login_required
def dashboard(request):
    context = {}
    return render(request, "dashboard.html", context)
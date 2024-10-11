import random
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .forms import LoginForm, SignUpForm
from cooking_data.models import Recipe, Rating, Category, RecipeCategory, Favorite
from cooking_data.utils import get_highest_rated_recipes, get_highest_rated_recipes_per_category, generate_pdf, get_random_recipes


def landing_page(request):
    context = {"featured_recipes": get_highest_rated_recipes(limit=3)}
    return render(request, "landing_page.html", context)


def recipes(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, "recipes.html", context)


def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    instructions = recipe.instructions.splitlines()
    existing_rating = Rating.objects.filter(user=request.user, recipe=recipe).first()
    existing_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    if request.method == 'POST':
        score = request.POST.get('score')
        favorite_action = request.POST.get('favorite')
        if score:
            Rating.objects.update_or_create(
                user=request.user,
                recipe=recipe,
                defaults={'score': score}
            )
        if favorite_action:
            if existing_favorite:
                Favorite.objects.filter(user=request.user, recipe=recipe).delete()
            else:
                Favorite.objects.create(user=request.user, recipe=recipe)

        return HttpResponseRedirect(request.path)

    context = {
        'recipe': recipe,
        'existing_rating': existing_rating,
        'existing_favorite': existing_favorite,
        'instructions': instructions
    }

    return render(request, 'recipe_detail.html', context)


def featured_recipes(request):
    context = {"featured_recipes": get_highest_rated_recipes(), 'category_recipes': get_highest_rated_recipes_per_category()}
    return render(request, "featured_recipes.html", context)


def search_recipes(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    results = Recipe.objects.all()
    if query and len(query) < 80:
        results = results.filter(name__icontains=query)
    if category:
        try:
            category_obj = Category.objects.get(name=category)
            results = results.filter(categories__category=category_obj).distinct()
        except Category.DoesNotExist:
            results = Recipe.objects.none()
    return render(request, 'search_recipes.html', {'results': results, 'query': query, 'category': category})


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


@login_required
def dashboard(request):
    if request.GET.get('randomize') == 'true':
        random_recipes = get_random_recipes()
        request.session['random_recipes'] = [recipe.id for recipe in random_recipes]
        return redirect('cooking_post:dashboard')

    recipe_ids = request.session.get('random_recipes')
    if recipe_ids:
        random_recipes = Recipe.objects.filter(id__in=recipe_ids)
    else:
        random_recipes = get_random_recipes()
        request.session['random_recipes'] = [recipe.id for recipe in random_recipes]

    shopping_list = defaultdict(float)

    for recipe in random_recipes:
        for recipe_ingredient in recipe.ingredients.all():
            ingredient_name = recipe_ingredient.ingredient.name
            quantity = recipe_ingredient.quantity or 0
            shopping_list[ingredient_name] += quantity

    if request.GET.get('pdf') == 'true':
        pdf = generate_pdf(shopping_list.items())
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shopping_list.pdf"'
        return response

    context = {
        "weekly_ideas": random_recipes,
        "shopping_list": shopping_list.items(),
    }
    return render(request, "dashboard.html", context)
from django.db.models import Avg, Max
from .models import Recipe, RecipeCategory, Category
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import random


def get_highest_rated_recipes(limit=3):
    max_rating = (
        Recipe.objects
        .annotate(average_rating=Avg('ratings__score'))
        .aggregate(max_avg_rating=Max('average_rating'))['max_avg_rating']
    )

    recipes = (
        Recipe.objects
        .annotate(average_rating=Avg('ratings__score'))
        .filter(average_rating=max_rating)[:limit]
    )

    return recipes


def get_highest_rated_recipes_per_category(limit=4):
    categories = Category.objects.all()
    category_recipes = {}

    for category in categories:
        recipes = (
            Recipe.objects
            .filter(categories__category=category)
            .annotate(average_rating=Avg('ratings__score'))
            .order_by('-average_rating')[:limit]
        )
        category_recipes[category.name] = recipes

    return category_recipes


def get_random_recipes(num_recipes=7):
    all_recipes = list(Recipe.objects.all())
    num_recipes = min(num_recipes, len(all_recipes))
    random_recipes = random.sample(all_recipes, num_recipes)
    return random_recipes


def generate_pdf(shopping_list):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Shopping List")
    y_position = 720
    max_y_position = 50

    for ingredient, quantity in shopping_list:
        if y_position < max_y_position:
            p.showPage()
            p.setFont("Helvetica", 12)
            p.drawString(100, 750, "Shopping List")
            y_position = 720

        p.drawString(100, y_position, f"{ingredient}")
        y_position -= 20

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
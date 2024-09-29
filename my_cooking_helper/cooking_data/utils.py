from django.db.models import Avg, Max
from .models import Recipe, RecipeCategory, Category

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
from django.db.models import Avg, Max
from .models import Recipe

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

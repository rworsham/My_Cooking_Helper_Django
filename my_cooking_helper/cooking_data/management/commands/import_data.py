import csv
import json
from django.core.management.base import BaseCommand
from cooking_data.models import Recipe, Ingredient, RecipeIngredient

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        count = 0

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if count >= 20:
                    break

                recipe_data = {
                    'title': row['title'],
                    'instructions': ' '.join(json.loads(row['directions'])),
                    'ingredients': json.loads(row['ingredients']),
                }

                recipe, created = Recipe.objects.get_or_create(
                    name=recipe_data['title'],
                    instructions=recipe_data['instructions'],
                )

                ingredients = recipe_data['ingredients']
                for ingredient_name in ingredients:
                    ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)

                    RecipeIngredient.objects.get_or_create(
                        recipe=recipe,
                        ingredient=ingredient,
                    )

                self.stdout.write(self.style.SUCCESS(f'Successfully imported {recipe.name}'))
                count += 1



# import csv                                KEEPING FOR TESTING
# import json
# from django.core.management.base import BaseCommand
#
# class Command(BaseCommand):
#     help = 'Import first 50 recipes from a CSV file'
#
#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', type=str)
#
#     def handle(self, *args, **kwargs):
#         csv_file = kwargs['csv_file']
#         count = 0
#
#         with open(csv_file, newline='', encoding='utf-8') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 if count >= 50:  # Stop after 50 entries
#                     break
#
#                 # Prepare recipe data
#                 recipe_data = {
#                     'title': row['title'],
#                     'directions': json.loads(row['directions']),
#                     'ingredients': json.loads(row['ingredients']),
#                 }
#
#                 # Print the recipe data
#                 self.stdout.write(self.style.SUCCESS(f"Recipe {count + 1}:"))
#                 self.stdout.write(f"Title: {recipe_data['title']}")
#                 self.stdout.write("Directions:")
#                 for step in recipe_data['directions']:
#                     self.stdout.write(f"- {step}")
#                 self.stdout.write("Ingredients:")
#                 for ingredient in recipe_data['ingredients']:
#                     self.stdout.write(f"- {ingredient}")
#                 self.stdout.write("")  # Add an empty line for spacing
#
#                 count += 1
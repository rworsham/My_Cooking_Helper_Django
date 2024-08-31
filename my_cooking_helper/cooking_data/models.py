from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField()
    preparation_time = models.DurationField(null=True, blank=True)
    cooking_time = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} in {self.recipe.name}"

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recipe', 'category')

    def __str__(self):
        return f"{self.recipe.name} is in category {self.category.name}"

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recipe', 'tag')

    def __str__(self):
        return f"{self.recipe.name} is tagged with {self.tag.name}"
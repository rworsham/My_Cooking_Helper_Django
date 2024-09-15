from django import forms
from .models import Ingredient, Recipe, RecipeIngredient, Category, RecipeCategory, Tag, RecipeTag

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'preparation_time', 'cooking_time']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 5}),
        }

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['recipe', 'ingredient', 'quantity', 'unit']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class RecipeCategoryForm(forms.ModelForm):
    class Meta:
        model = RecipeCategory
        fields = ['recipe', 'category']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class RecipeTagForm(forms.ModelForm):
    class Meta:
        model = RecipeTag
        fields = ['recipe', 'tag']
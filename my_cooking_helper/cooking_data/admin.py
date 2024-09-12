from django.contrib import admin
from .models import Ingredient, RecipeIngredient, Recipe, RecipeTag, RecipeCategory, Category, Tag

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeCategoryInline(admin.TabularInline):
    model = RecipeCategory
    extra = 1

class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline, RecipeCategoryInline, RecipeTagInline]
    list_display = ('name', 'preparation_time', 'cooking_time')
    search_fields = ('name',)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity', 'unit')
    search_fields = ('recipe__name', 'ingredient__name')

class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'category')
    search_fields = ('recipe__name', 'category__name')

class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'tag')
    search_fields = ('recipe__name', 'tag__name')

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(RecipeCategory, RecipeCategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
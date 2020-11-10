from django.contrib import admin
from .models import Category, Recipe, Ingredient, OwnedIngredient

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(OwnedIngredient)
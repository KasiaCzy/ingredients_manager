from django.urls import path
from . import views


app_name = 'manage_ingredients'
urlpatterns = [
    path('', views.main, name='main'),
    path('ingredients/', views.ingredients_list, name='ingredients_list'),
    path('ingredients/<int:ingredient_id>', views.owned_ingredients, name='owned_ingredients'),
    path('ingredients/<int:ingredient_id>/add_owned_ingredient', views.add_owned_ingredient,
         {'redirect_url': 'manage_ingredients:owned_ingredients',
          'url_name': 'manage_ingredients:add_owned_ingredient_id'}, name='add_owned_ingredient_id'),
    path('recipes/', views.recipes_list, name='recipes'),
    path('use_up_today/', views.use_up_today_list, name='use_up_today'),
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('edit_ingredient/<int:ingredient_id>/', views.edit_ingredient, name='edit_ingredient'),
    path('delete_ingredient/<int:ingredient_id>/', views.delete_ingredient, name='delete_ingredient'),
    path('add_owned_ingredient/<int:ingredient_id>', views.add_owned_ingredient,
         {'redirect_url': 'manage_ingredients:ingredients_list', 'url_name': 'manage_ingredients:add_owned_ingredient'},
         name='add_owned_ingredient'),
    path('edit_owned_ingredient/<int:ownedingredient_id>/', views.edit_owned_ingredient,
         {'redirect_url': 'manage_ingredients:owned_ingredients', 'url_name': 'manage_ingredients:edit_owned_ingredient'},
         name='edit_owned_ingredient'),
    path('delete_owned_ingredient/<int:ownedingredient_id>/', views.delete_owned_ingredient,
         {'redirect_url': 'manage_ingredients:owned_ingredients', 'url_name': 'manage_ingredients:owned_ingredients'},
         name='delete_owned_ingredient'),
    path('use_up_today/edit_owned_ingredient/<int:ownedingredient_id>/', views.edit_owned_ingredient,
         {'redirect_url': 'manage_ingredients:use_up_today', 'url_name': 'manage_ingredients:edit_owned_ingredient_use_up'},
         name='edit_owned_ingredient_use_up'),
    path('use_up_today/delete_owned_ingredient/<int:ownedingredient_id>/', views.delete_owned_ingredient,
         {'redirect_url': 'manage_ingredients:use_up_today', 'url_name': 'manage_ingredients:use_up_today'},
         name='delete_owned_ingredient_use_up'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('get_recipes/<int:ingredient_id>/', views.get_recipes, name='get_recipes'),
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('categories/', views.categories_list, name='categories_list'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
]

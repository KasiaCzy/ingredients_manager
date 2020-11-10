from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db import IntegrityError
from django.db.models import Sum
from datetime import date, timedelta
from django.forms import modelformset_factory
from .models import Category, Recipe, Ingredient, OwnedIngredient
from .forms import AddIngredientForm, EditIngredientForm, AddOwnedIngredientForm, EditOwnedIngredientForm,\
    AddRecipeForm, EditRecipeForm, ManageCategoryForm
from .filters import IngredientFilter, RecipeFilter


def check_owner(owner, user):
    if owner != user:
        raise Http404


def main(request):
    return render(request, 'manage_ingredients/main.html')


@login_required
def ingredients_list(request):
    ingredients = Ingredient.objects.filter(owner=request.user).annotate(total=Sum('ownedingredient__quantity'))

    ingredient_filter = IngredientFilter(request.GET, request=request, queryset=ingredients)
    ingredients = ingredient_filter.qs

    context = {'ingredients': ingredients, 'filter': ingredient_filter}
    return render(request, 'manage_ingredients/ingredients_list.html', context)


@login_required
def owned_ingredients(request, ingredient_id):
    ingredient = Ingredient.objects.filter(owner=request.user).get(id=ingredient_id)
    owned_ingredient = ingredient.ownedingredient_set.order_by('best_before')

    context = {'ingredient': ingredient, 'owned_ingredient': owned_ingredient}
    return render(request, 'manage_ingredients/owned_ingredient.html', context)


@login_required
def recipes_list(request):
    recipes = Recipe.objects.filter(owner=request.user)
    recipes_filter = RecipeFilter(request.GET, request=request, queryset=recipes)
    recipes = recipes_filter.qs

    context = {'recipes': recipes, 'filter': recipes_filter}
    return render(request, 'manage_ingredients/recipes.html', context)


@login_required
def use_up_today_list(request):
    today = date.today()
    should_use = OwnedIngredient.objects.filter(owner=request.user).filter(quantity__gt=0)\
        .filter(best_before__lte=today + timedelta(days=2), best_before__gte=today)
    passed_date = OwnedIngredient.objects.filter(owner=request.user).filter(quantity__gt=0)\
        .filter(best_before__lte=today)

    context = {'should_use': should_use, 'passed_date': passed_date}
    return render(request, 'manage_ingredients/use_up_today.html', context)


@login_required
def add_ingredient(request):
    e = None
    if request.method != 'POST':
        form = AddIngredientForm()
    else:
        form = AddIngredientForm(data=request.POST)
        if form.is_valid():
            try:
                added_ingredient = form.save(commit=False)
                added_ingredient.owner = request.user
                added_ingredient.save()
                return redirect('manage_ingredients:ingredients_list')
            except IntegrityError:
                e = 'The name must be unique. Ingredient with this name already exists.'

    context = {'form': form, 'url_name': 'manage_ingredients:add_ingredient',
               'url_back': 'manage_ingredients:ingredients_list', 'title': 'Add ingredient', 'e': e}
    return render(request, 'manage_ingredients/add.html', context)


@login_required
def edit_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    check_owner(ingredient.owner, request.user)
    if request.method != 'POST':
        form = EditIngredientForm(instance=ingredient)
    else:
        form = EditIngredientForm(instance=ingredient, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('manage_ingredients:ingredients_list')
            except IntegrityError:
                pass

    context = {'object': ingredient, 'form': form, 'url_name': 'manage_ingredients:edit_ingredient',
               'url_cancel': 'manage_ingredients:ingredients_list'}
    return render(request, 'manage_ingredients/edit.html', context)


@login_required
def delete_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    check_owner(ingredient.owner, request.user)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('manage_ingredients:ingredients_list')

    context = {'ingredient': ingredient, 'url_name': 'manage_ingredients:ingredients_list', 'name': 'ingredient',
               'field': ingredient.name}
    return render(request, 'manage_ingredients/delete.html', context)


@login_required
def add_owned_ingredient(request, ingredient_id, redirect_url, url_name):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    if request.method != 'POST':
        form = AddOwnedIngredientForm()
    else:
        form = AddOwnedIngredientForm(data=request.POST)
        if form.is_valid():
            added_item = form.save(commit=False)
            added_item.ingredient_name = ingredient
            added_item.owner = request.user
            added_item.save()
            if redirect_url == 'manage_ingredients:owned_ingredients':
                return redirect(redirect_url, ingredient_id=ingredient_id)
            else:
                return redirect(redirect_url)

    context = {'object': ingredient.id, 'ingredient': ingredient, 'form': form,
               'url_name': url_name,
               'url_back': 'manage_ingredients:ingredients_list', 'title': ingredient.name}
    return render(request, 'manage_ingredients/add.html', context)


@login_required
def edit_owned_ingredient(request, ownedingredient_id, redirect_url, url_name):
    owned_ingredient = OwnedIngredient.objects.get(id=ownedingredient_id)
    ingredient_id = owned_ingredient.ingredient_name.id
    check_owner(owned_ingredient.owner, request.user)
    if request.method != 'POST':
        form = EditOwnedIngredientForm(instance=owned_ingredient)
    else:
        form = EditOwnedIngredientForm(instance=owned_ingredient, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                if redirect_url == 'manage_ingredients:owned_ingredients':
                    return redirect(redirect_url, ingredient_id=ingredient_id)
                else:
                    return redirect(redirect_url)
            except IntegrityError:
                pass
    if redirect_url == 'manage_ingredients:owned_ingredients':
        context = {'object': owned_ingredient, 'form': form, 'url_name': url_name,
                   'url_cancel': redirect_url, 'object_cancel': ingredient_id}
    else:
        context = {'object': owned_ingredient, 'form': form, 'url_name': url_name,
                   'url_cancel': redirect_url}
    return render(request, 'manage_ingredients/edit.html', context)


@login_required
def delete_owned_ingredient(request, ownedingredient_id, redirect_url, url_name):
    owned_ingredient = OwnedIngredient.objects.get(id=ownedingredient_id)
    ingredient_id = owned_ingredient.ingredient_name.id
    check_owner(owned_ingredient.owner, request.user)
    if request.method == 'POST':
        owned_ingredient.delete()
        if redirect_url == 'manage_ingredients:owned_ingredients':
            return redirect(redirect_url, ingredient_id=ingredient_id)
        else:
            return redirect(redirect_url)
    if redirect_url == 'manage_ingredients:owned_ingredients':
        context = {'ingredient': owned_ingredient, 'url_name': url_name,
                   'object': ingredient_id, 'name': owned_ingredient.ingredient_name,
                   'field': owned_ingredient.quantity}
    else:
        context = {'ingredient': owned_ingredient, 'url_name': url_name,
                   'name': 'ingredient', 'field': owned_ingredient.quantity}
    return render(request, 'manage_ingredients/delete.html', context)


@login_required
def add_recipe(request):
    e = None
    if request.method != 'POST':
        form = AddRecipeForm()
    else:
        form = AddRecipeForm(data=request.POST)
        if form.is_valid():
            try:
                added_recipe = form.save(commit=False)
                added_recipe.owner = request.user
                added_recipe.save()
                form.save_m2m()
                return redirect('manage_ingredients:recipes')
            except IntegrityError:
                e = 'The name must be unique. Recipe with this name already exists.'

    context = {'form': form, 'url_name': 'manage_ingredients:add_recipe', 'url_back': 'manage_ingredients:recipes',
               'title': 'Add recipe', 'e': e}
    return render(request, 'manage_ingredients/add.html', context)


@login_required
def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    check_owner(recipe.owner, request.user)
    if request.method != 'POST':
        form = EditRecipeForm(instance=recipe)
    else:
        form = EditRecipeForm(instance=recipe, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('manage_ingredients:recipes')
            except IntegrityError:
                pass

    context = {'object': recipe, 'form': form, 'url_name': 'manage_ingredients:edit_recipe',
               'url_cancel': 'manage_ingredients:recipes'}
    return render(request, 'manage_ingredients/edit.html', context)


@login_required
def delete_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    check_owner(recipe.owner, request.user)
    if request.method == 'POST':
        recipe.delete()
        return redirect('manage_ingredients:recipes')

    context = {'recipe': recipe, 'url_name': 'manage_ingredients:recipes', 'name': 'recipe',
               'field': recipe.title}
    return render(request, 'manage_ingredients/delete.html', context)


@login_required
def get_recipes(request, ingredient_id):
    recipes = Recipe.objects.filter(owner=request.user).filter(ingredient=ingredient_id)
    ingredient = Ingredient.objects.filter(owner=request.user).get(id=ingredient_id)

    context = {'recipes': recipes, 'ingredient': ingredient}
    return render(request, 'manage_ingredients/get_recipes.html', context)


@login_required
def manage_categories(request):
    CategoryFormSet = modelformset_factory(Category, form=ManageCategoryForm, extra=3, max_num=10)
    categories = Category.objects.filter(owner=request.user)
    if request.method != 'POST':
        formset = CategoryFormSet(queryset=categories)
    else:
        formset = CategoryFormSet(queryset=categories, data=request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.owner = request.user
                instance.save()
            return redirect('manage_ingredients:ingredients_list')

    context = {'formset': formset, 'title': 'Manage categories'}
    return render(request, 'manage_ingredients/manage_categories.html', context)


@login_required
def categories_list(request):
    categories = Category.objects.filter(owner=request.user)

    context = {'categories': categories}
    return render(request, 'manage_ingredients/categories_list.html', context)


@login_required
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    check_owner(category.owner, request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('manage_ingredients:categories_list')

    context = {'category': category, 'url_name': 'manage_ingredients:categories_list', 'name': 'category',
               'field': category.name}
    return render(request, 'manage_ingredients/delete.html', context)

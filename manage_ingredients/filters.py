import django_filters
from django import forms

from .models import Category, Ingredient


def categories(request):

    if request is None:
        return Category.objects.none()

    return Category.objects.filter(owner=request.user)


def ingredients(request):

    if request is None:
        return Ingredient.objects.none()

    return Ingredient.objects.filter(owner=request.user)


class IngredientFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        label='Category',
        widget=forms.Select(attrs={'class': 'form-control mr-3'}), queryset=categories
    )
    name = django_filters.CharFilter(
        label='Ingredient name', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search by name', 'class': 'form-control'})
    )


class RecipeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        label='Recipe name', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search by name', 'class': 'form-control mr-3'})
    )
    ingredient = django_filters.ModelMultipleChoiceFilter(
        label='Ingredient',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}), queryset=ingredients,
    )
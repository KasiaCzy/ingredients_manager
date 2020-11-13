from django import forms
from .models import Ingredient, OwnedIngredient, Category, Recipe


class DateInput(forms.DateInput):
    input_type = 'date'


class AddIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit', 'category']


class EditIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit', 'category']


class AddOwnedIngredientForm(forms.ModelForm):
    class Meta:
        model = OwnedIngredient
        fields = ['quantity', 'best_before', 'note']
        widgets = {
            'best_before': DateInput()
        }


class EditOwnedIngredientForm(forms.ModelForm):
    class Meta:
        model = OwnedIngredient
        fields = ['quantity', 'best_before', 'note']
        widgets = {
            'best_before': DateInput()
        }


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'link', 'ingredient']
        widgets = {
            'ingredient': forms.CheckboxSelectMultiple()
        }


class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'link', 'ingredient']
        widgets = {
            'ingredient': forms.CheckboxSelectMultiple()
        }


class ManageCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Edit/Add category'}
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Add new category'})
        }
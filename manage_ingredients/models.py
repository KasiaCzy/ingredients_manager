from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'categories'

        constraints = [
            models.UniqueConstraint(fields=['name', 'owner_id'], name='unique_name_category'),
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    UNIT = [
        ('ML', 'ml'),
        ('G', 'g'),
        ('PCS', 'pcs.'),
    ]
    name = models.CharField(max_length=32)
    unit = models.CharField(max_length=5, choices=UNIT)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner_id'], name='unique_name_ingredient'),
        ]

    def __str__(self):
        return self.name


class OwnedIngredient(models.Model):
    tip = models.CharField(max_length=16, default='...')
    quantity = models.FloatField(default=0)
    best_before = models.DateField()
    ingredient_name = models.ForeignKey(Ingredient, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Recipe(models.Model):
    title = models.CharField(max_length=32)
    link = models.URLField(max_length=200)
    ingredient = models.ManyToManyField(Ingredient, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'owner_id'], name='unique_name_recipe'),
        ]

    def __str__(self):
        return self.title

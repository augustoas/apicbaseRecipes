from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


# Models

class Ingredient(models.Model):
    user = models.ForeignKey('auth.User', related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0)
    unit = models.CharField(max_length=200)

    class Meta:
        unique_together = (("user", "name"),) 

class Recipe(models.Model):
    user = models.ForeignKey('auth.User', related_name='recipes', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    class Meta:
        unique_together = (("user", "name"),) 

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    r_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=False)

    class Meta:
        unique_together =[['recipe','ingredient']]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
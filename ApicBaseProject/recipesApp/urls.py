from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('', views.apiEndPoints, name='apiEndPoints'),

    path('users', views.users, name='users'),
    path('register', views.register, name='register'),
    path('login', obtain_auth_token, name='login'),


    path('ingredient-list', views.ingredientsList, name='ingredient-list'),
    path('ingredient/<str:pk>', views.ingredientById, name='ingredient'),
    path('ingredient-new', views.newIngredient, name='ingredient-new'),
    path('ingredient-edit/<str:pk>', views.editIngredient, name='ingredient-edit'),
    path('ingredient-delete/<str:pk>', views.deleteIngredient, name='ingredient-delete'),
    
    path('recipe-list', views.recipeList, name='recipe-list'),
    path('recipe-new', views.newRecipe, name='recipe-new'),
    path('recipe-edit/<str:pk>', views.editRecipe, name='recipe-edit'),
    path('recipe-delete/<str:pk>', views.deleteRecipe, name='recipe-delete'),

    
    path('recipe-ingredients-list', views.recipeIngredientsList, name='recipe-ingredient-list'),
    path('new-recipe-ingredient', views.addIngredientToRecipe, name='new-recipe-ingredient'),
    path('ingredient-recipe-delete/<str:pk>', views.deleteIngredientFromRecipe, name='ingredient-recipe-delete'),
    path('ingredient-recipe-edit/<str:pk>', views.editIngredientFromRecipe, name='ingredient-recipe-edit'),

]
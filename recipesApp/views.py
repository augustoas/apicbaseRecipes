from copyreg import constructor
from pickle import TRUE
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Ingredient, Recipe, RecipeIngredient
from .serializers import UserSerializer, IngredientSerializer, NewIngredientSerializer, EditIngredientSerializer, RecipeSerializer, NewRecipeSerializer, EditRecipeSerializer, NewIngredientToRecipe, EditIngredientRecipeSerializer, IngredientRecipe, RegistrationSerializer

@api_view(['GET'])
def apiEndPoints(request):
    api_urls = {
        'Recipes List': '/recipes-list',
        'Recipe Detail': '/recipe-detail/<str:pk>',
        'Ingredients List': '/ingredients-list',
    }
    return Response(api_urls)

#USERS

@api_view(['GET'])
def users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        data['response'] = "new user registered"
        data['username'] = user.username
        data['token'] = token
        data['ok'] = True
    else:
        data['errors'] = serializer.errors
        data['ok'] = False

    return Response(data)

#INGREDIENTS

#INGREDIENTS FILTERED BY USER
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def ingredientsList(request):
    user = request.user
    ingredients = Ingredient.objects.filter(user=user)
    serializer = IngredientSerializer(ingredients, many=True)

    return Response(serializer.data)

#INGREDIENT BY ID (NOT USED)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def ingredientById(request, pk):
    ingredients = Ingredient.objects.get(id=pk)
    serializer = IngredientSerializer(ingredients, many=False)

    return Response(serializer.data)

#NEW INGREDIENT
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def newIngredient(request):
    serializer = NewIngredientSerializer(data=request.data, context={'request':request})
    data = {}
    if serializer.is_valid():
        ingredient = serializer.save()
        data['response'] = "new ingredient registered "+ingredient.name
        data['ingredient'] = serializer.data
        data['ok'] = True
    else:
        data = serializer.errors
    return Response(data)

#EDIT INGREDIENT
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def editIngredient(request, pk):
    data = {}
    try: 
        ingredient = Ingredient.objects.get(id=pk)
    except Ingredient.DoesNotExist:
        data['response'] = "ingredient not exist"
        return Response(data)

    serializer = EditIngredientSerializer(ingredient, data=request.data)
    if serializer.is_valid():        
        serializer.save()
        data['response'] = "ingredient edited"
        data['ingredient'] = serializer.data
        data['ok'] = True
    else:
        data['response'] = "ingredient not edited"
        data['ok'] = False
        data = serializer.errors
    return Response(data)
    
    
#DELETE INGREDIENT
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteIngredient(request, pk):
    data = {}
    try: 
        ingredient = Ingredient.objects.get(id=pk)
    except Ingredient.DoesNotExist:
        data['response'] = "ingredient not exist"
        return Response(data)
    
    operation = ingredient.delete()
    if operation:        
        data['response'] = "ingredient deleted succesfully"
        data['ok'] = True
    else:
        data['response'] = "ingredient not deleted"
    return Response(data)

#RECIPES

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def recipeList(request):
    user = request.user
    recipes = Recipe.objects.filter(user=user)
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)

#NEW RECIPE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def newRecipe(request):
    serializer = NewRecipeSerializer(data=request.data, context={'request':request})
    data = {}
    if serializer.is_valid():
        recipe = serializer.save()
        data['response'] = "new recipe registered "+recipe.name
        data['recipe'] = serializer.data
        data['ok'] = True
    else:
        data = serializer.errors
    return Response(data)

#EDIT RECIPE
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def editRecipe(request, pk):
    data = {}
    try: 
        recipe = Recipe.objects.get(id=pk)
    except Recipe.DoesNotExist:
        data['response'] = "recipe not exist"
        return Response(data)
    
    serializer = EditRecipeSerializer(recipe, data=request.data)
    if serializer.is_valid():        
        serializer.save()
        data['response'] = "recipe edited"
        data['recipe'] = serializer.data
        data['ok'] = True
    else:
        data['response'] = "recipe not edited"
        data['ok'] = False
        data = serializer.errors
    return Response(data)

#DELETE RECIPE
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteRecipe(request, pk):
    data = {}
    try: 
        recipe = Recipe.objects.get(id=pk)
    except Recipe.DoesNotExist:
        data['response'] = "recipe not exist in recipe"
        return Response(data)
    
    operation = recipe.delete()
    if operation:        
        data['response'] = "recipe deleted succesfully"
    else:
        data['response'] = "recipe not deleted"
    return Response(data)

#INGREDIENTS RECIPES RELATION LIST
@api_view(['GET'])
def recipeIngredientsList(request):
    ingrec = RecipeIngredient.objects.all()
    serializer = NewIngredientToRecipe(ingrec, many=True)
    return Response(serializer.data)

#INGREDIENTS BY RECIPE PK
@api_view(['GET'])
def ingredientsByRecipeList(request, pk):
    recipe = Recipe.objects.get(id=pk)
    ingrec = RecipeIngredient.objects.filter(recipe=recipe)
    serializer = NewIngredientToRecipe(ingrec, many=True)
    return Response(serializer.data)

#ADD INGREDIENT TO RECIPE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def addIngredientToRecipe(request):
    serializer = IngredientRecipe(data=request.data)
    data = {}
    print('REQUEST', request.data)
    if serializer.is_valid():
        ingredient = serializer.save()
        data['response'] = "new ingredient added to recipe"
        data['ingrec'] = serializer.data
        data['ok'] = True
    else:
        print('no es valido')
        data['response'] = "failed"
        data['ok'] = False
        data['error']= serializer.errors

    return Response(data)

#EDIT INGREDIENT FROM RECIPE
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def editIngredientFromRecipe(request, pk):
    data = {}
    try: 
        ingredient = RecipeIngredient.objects.get(id=pk)
    except RecipeIngredient.DoesNotExist:
        data['response'] = "ingredient not exist"
        return Response(data)
    
    serializer = EditIngredientRecipeSerializer(ingredient, data=request.data)
    if serializer.is_valid():        
        serializer.save()
        data['response'] = "ingredient from recipe edited"
        data['ok'] = True
    else:
        data['response'] = "ingredient from recipe not edited"
        data = serializer.errors
    return Response(data)

#DELETE INGREDIENT FROM RECIPE
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteIngredientFromRecipe(request, pk):
    print('request dta', request.data)
    data = {}
    try: 
        ingredient = RecipeIngredient.objects.get(id=pk)
    except RecipeIngredient.DoesNotExist:
        data['response'] = "ingredient not exist in recipe"
        return Response(data)
    
    operation = ingredient.delete()
    if operation:        
        data['response'] = "ingredient deleted succesfully"
        data['ok'] = True
    else:
        data['response'] = "ingredient not deleted"
    return Response(data)


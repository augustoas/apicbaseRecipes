from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Ingredient, Recipe, RecipeIngredient
from .serializers import UserSerializer, IngredientSerializer, NewIngredientSerializer, EditIngredientSerializer, RecipeSerializer, NewRecipeSerializer, EditRecipeSerializer, NewIngredientToRecipe, EditIngredientRecipeSerializer, RegistrationSerializer

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
        data['response'] = "new user registered"
        data['username'] = user.username
        token = Token.objects.get(user=user).key
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)

#INGREDIENTS

#NO VA 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def ingredientsList(request):
    ingredients = Ingredient.objects.all()
    serializer = IngredientSerializer(ingredients, many=True)

    return Response(serializer.data)

#NO VA
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
        data['response'] = "new ingredient registered"
        data['name'] = ingredient.name
    else:
        data = serializer.errors

    return Response(data)

#EDIT INGREDIENT
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def editIngredient(request, pk):
    print('edit ingredient')
    print('request', request)

    data = {}
    try: 
        ingredient = Ingredient.objects.get(id=pk)
        #if tokens son iguales, que procesa, osino que tire error .
    except Ingredient.DoesNotExist:
        data['response'] = "ingredient not exist"
        return Response(data)

    serializer = EditIngredientSerializer(ingredient, data=request.data)
    if serializer.is_valid():        
        serializer.save()
        data['response'] = "ingredient edited"
    else:
        data['response'] = "ingredient not edited"
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
    else:
        data['response'] = "ingredient not deleted"
    return Response(data)

#RECIPES

#NO VA
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def recipeList(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)

#CREATE RECIPE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def newRecipe(request):
    serializer = NewRecipeSerializer(data=request.data, context={'request':request})
    data = {}
    if serializer.is_valid():
        recipe = serializer.save()
        data['response'] = "new recipe registered"
        data['name'] = recipe.name
    else:
        print('no es valido')
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
    else:
        data['response'] = "recipe not edited"
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

#NO VA
@api_view(['GET'])
def recipeIngredientsList(request):
    ingredients = RecipeIngredient.objects.all()
    serializer = NewIngredientToRecipe(ingredients, many=True)
    return Response(serializer.data)

#ADD INGREDIENT TO RECIPE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def addIngredientToRecipe(request):
    serializer = NewIngredientToRecipe(data=request.data)
    data = {}
    if serializer.is_valid():
        ingredient = serializer.save()
        data['response'] = "new ingredient added to recipe"
    else:
        data = serializer.errors
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
    else:
        data['response'] = "ingredient from recipe not edited"
        data = serializer.errors
    return Response(data)

#DELETE INGREDIENT FROM RECIPE
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteIngredientFromRecipe(request, pk):
    data = {}
    try: 
        ingredient = RecipeIngredient.objects.get(id=pk)
    except RecipeIngredient.DoesNotExist:
        data['response'] = "ingredient not exist in recipe"
        return Response(data)
    
    operation = ingredient.delete()
    if operation:        
        data['response'] = "ingredient deleted succesfully"
    else:
        data['response'] = "ingredient not deleted"
    return Response(data)


import token
from rest_framework import serializers
from .models import Recipe, Ingredient, RecipeIngredient
from django.contrib.auth.models import User

#INGREDIENTS

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'

class NewIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ['user'] # set user as read-only field

    def create(self, validated_data):
        # get the user from the request
        user = self.context['request'].user
        return Ingredient.objects.create(user=user, **validated_data)

class EditIngredientSerializer(NewIngredientSerializer):
    class Meta:
        model = Ingredient
        fields = ('articleNumber' ,'name' , 'cost', 'unit', 'amount')

#RECIPES

class RecipeSerializer(serializers.ModelSerializer):

    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

class NewRecipeSerializer(serializers.ModelSerializer):
    
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['user'] # set user as read-only field

    def create(self, validated_data):
        # get the user from the request
        user = self.context['request'].user
        return Recipe.objects.create(user=user, **validated_data)

class EditRecipeSerializer(NewRecipeSerializer):

    class Meta:
        model = Recipe
        fields = ('name', 'ingredients')

class IngredientRecipe(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = '__all__'

class NewIngredientToRecipe(serializers.ModelSerializer):

    ingredient = IngredientSerializer(required = False)
    recipe = RecipeSerializer(required = False)

    class Meta:
        model = RecipeIngredient
        fields = '__all__'

class EditIngredientRecipeSerializer(NewIngredientToRecipe):

    class Meta:
        model = RecipeIngredient
        fields = '__all__'

#USER

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'ingredients', 'recipes']

class RegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input-type':'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        user = User(
            username = self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        
        user.set_password(password)
        user.save()
        return user
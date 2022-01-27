from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient

# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_ingredients')
    def get_ingredients(self, obj):
        return "\n".join([i.name for i in obj.ingredients.all()])


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'articleNumber' , 'name', 'cost', 'unit')

class RecipeIngredientAdmin(admin.ModelAdmin):
    pass

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)



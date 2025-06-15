from django.contrib import admin

from cookbook.models import (
    Ingredient,
    IngredientTranslation,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    Step,
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("key", "calories_per_100g")
    search_fields = ("key",)
    list_filter = ("calories_per_100g",)
    fieldsets = ((None, {"fields": ("key", "calories_per_100g")}),)
    ordering = ("key",)


@admin.register(IngredientTranslation)
class IngredientTranslationAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "language", "name")
    search_fields = ("ingredient__key", "name")
    list_filter = ("language",)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class StepInline(admin.TabularInline):
    model = Step
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    search_fields = ("title", "author__username")
    list_filter = ("author", "created_at")
    inlines = [RecipeIngredientInline, StepInline]
    readonly_fields = ("created_at",)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount", "unit")
    search_fields = ("recipe__title", "ingredient__key")
    list_filter = ("unit",)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ("recipe", "order", "description")
    search_fields = ("recipe__title", "description")


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ("key", "get_name", "get_description")
    search_fields = ("key",)

    @staticmethod
    def get_name(obj):
        return str(obj.name)

    get_name.short_description = "Name"

    @staticmethod
    def get_description(obj):
        return str(obj.description)

    get_description.short_description = "Description"

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# Predefined localized recipe tags constant with name and description
PREDEFINED_TAGS = {
    "healthy": {
        "name": _("Healthy lifestyle"),
        "description": _("Low calorie, fiber rich"),
    },
    "quick": {
        "name": _("Quick"),
        "description": _("Prepares in 15–30 minutes"),
    },
    "cheap": {
        "name": _("Very affordable"),
        "description": _("Inexpensive ingredients"),
    },
    "holiday": {
        "name": _("Holiday"),
        "description": _("Suitable for special occasions"),
    },
    "vegan": {
        "name": _("Vegan"),
        "description": _("No animal products"),
    },
    "vegetarian": {
        "name": _("Vegetarian"),
        "description": _("No meat, may contain eggs/dairy"),
    },
    "gluten_free": {
        "name": _("Gluten-free"),
        "description": _("No wheat, barley, etc."),
    },
    "high_protein": {
        "name": _("High protein"),
        "description": _("Sports, protein-rich"),
    },
    "low_carb": {
        "name": _("Low carb"),
        "description": _("Suitable for keto diet"),
    },
    "traditional": {
        "name": _("Traditional"),
        "description": _("National and classic dishes"),
    },
    "experimental": {
        "name": _("Experimental"),
        "description": _("Unusual, creative"),
    },
    "children_friendly": {
        "name": _("Children-friendly"),
        "description": _("Mild taste, simple, no spicy"),
    },
    "spicy": {
        "name": _("Spicy"),
        "description": _("Hot and spicy"),
    },
    "breakfast": {
        "name": _("Breakfast"),
        "description": _("Morning dishes"),
    },
    "lunch": {
        "name": _("Lunch"),
        "description": _("Main midday dish"),
    },
    "dinner": {
        "name": _("Dinner"),
        "description": _("Evening dishes"),
    },
    "dessert": {
        "name": _("Dessert"),
        "description": _("Sweet dishes"),
    },
    "snack": {
        "name": _("Snack"),
        "description": _("Light meal or quick bite"),
    },
    "street_food": {
        "name": _("Street food"),
        "description": _("Popular food sold in public places"),
    },
    "comfort_food": {
        "name": _("Comfort food"),
        "description": _("Familiar, nostalgic, feel-good dishes"),
    },
    "low_effort": {
        "name": _("Low effort"),
        "description": _("Minimal cooking or prep needed"),
    },
    "high_calorie": {
        "name": _("High calorie"),
        "description": _("Dense and filling dishes"),
    },
}


class Ingredient(models.Model):
    key = models.CharField(max_length=100, unique=True, db_index=True)
    calories_per_100g = models.DecimalField(
        _("Calories per 100g/ml"),
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Enter the energy value per 100g or 100ml of the product."),
    )

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")


class IngredientTranslation(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="translations")
    language = models.CharField(max_length=10, choices=settings.LANGUAGES)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("ingredient", "language")
        verbose_name = _("Ingredient translation")
        verbose_name_plural = _("Ingredient translations")

    def __str__(self):
        return f"{self.name} ({self.language})"


class Recipe(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_language = models.CharField(max_length=10, choices=settings.LANGUAGES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    tags = models.ManyToManyField("RecipeTag", blank=True, related_name="recipes")

    def clean(self):
        if Recipe.objects.exclude(pk=self.pk).filter(author=self.author, title__iexact=self.title).exists():
            raise ValidationError({"title": _("You already have a recipe titled '%(title)s'.") % {"title": self.title}})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title[:1].upper() + self.title[1:]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["author", "title"], name="unique_recipe_title_per_author"),
        ]
        indexes = [
            models.Index(fields=["author", "title"]),
            models.Index(fields=["title"]),
            models.Index(fields=["created_at"]),
        ]
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")


class RecipeTranslation(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="translations")
    language = models.CharField(max_length=10, choices=settings.LANGUAGES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("recipe", "language")
        verbose_name = _("Recipe translation")
        verbose_name_plural = _("Recipe translations")

    def __str__(self):
        return f"{self.title} ({self.language})"


class RecipeIngredient(models.Model):
    class Unit(models.TextChoices):
        GRAM = "g", _("gram")
        KILOGRAM = "kg", _("kilogram")
        MILLILITER = "ml", _("milliliter")
        LITER = "l", _("liter")
        PIECE = "pcs", _("piece")
        TABLESPOON = "tbsp", _("tablespoon")
        TEASPOON = "tsp", _("teaspoon")
        CUP = "cup", _("cup")

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients", db_index=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, db_index=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=10, choices=Unit.choices)

    def __str__(self):
        return f"{self.amount} {self.get_unit_display()} {self.ingredient.key}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=["recipe", "ingredient"], name="unique_recipe_ingredient")]
        indexes = [
            models.Index(fields=["ingredient"]),
            models.Index(fields=["recipe"]),
        ]
        verbose_name = _("Recipe ingredient")
        verbose_name_plural = _("Recipe ingredients")


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="steps")
    order = models.PositiveIntegerField()
    description = models.TextField()

    def clean(self):
        if Step.objects.exclude(pk=self.pk).filter(recipe=self.recipe, order=self.order).exists():
            raise ValidationError(
                {"order": _("Step number %(order)s already exists for this recipe.") % {"order": self.order}}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Step {self.order} for {self.recipe.title}"

    class Meta:
        verbose_name = _("Step")
        verbose_name_plural = _("Steps")
        ordering = ["order"]
        constraints = [models.UniqueConstraint(fields=["recipe", "order"], name="unique_order_per_recipe")]


class RecipeTag(models.Model):
    """
    Fixed recipe tags stored by unique key.
    Names and descriptions localized via PREDEFINED_TAGS dict.
    """

    key = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return str(PREDEFINED_TAGS.get(self.key, {}).get("name", self.key))

    @property
    def description(self):
        return str(PREDEFINED_TAGS.get(self.key, {}).get("description", ""))

    class Meta:
        verbose_name = _("Recipe tag")
        verbose_name_plural = _("Recipe tags")

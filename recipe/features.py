from recipe.models import Recipe,Tag
from django.db.models import Q

def get_similar_recipes(self):
        """
        Returns a list of recipes that have similar tags, sorted by the number of matching tags.
        """
        similar_recipes = Recipe.objects.filter(tags__in=self.tags.all()).exclude(id=self.id).distinct()
        # Calculate the number of matching tags for each recipe
        recipe_tag_counts = {}
        for recipe in similar_recipes:
            common_tags = recipe.tags.filter(id__in=self.tags.all())
            recipe_tag_counts[recipe] = common_tags.count()
        # Sort the recipes based on the number of matching tags
        sorted_recipes = sorted(recipe_tag_counts, key=recipe_tag_counts.get, reverse=True)
        return sorted_recipes

def get_similar_recipes_by_tags(tag_names):
    """
    Returns a list of recipes that have similar tags to the provided tag names, sorted by the number of matching tags.
    """
    tags = Tag.objects.filter(name__in=tag_names)  # Get tags based on provided tag names
    similar_recipes = Recipe.objects.filter(tags__in=tags).distinct()
    # Calculate the number of matching tags for each recipe
    recipe_tag_counts = {}
    for recipe in similar_recipes:
        common_tags = recipe.tags.filter(id__in=tags)
        recipe_tag_counts[recipe] = common_tags.count()

    # Sort the recipes based on the number of matching tags
    sorted_recipes = sorted(recipe_tag_counts, key=recipe_tag_counts.get, reverse=True)

    return sorted_recipes




def search_recipes(query):
    """
    Returns a list of recipes that match the provided query in title, ingredients, tags, or instructions.
    """
    recipes = Recipe.objects.filter(
        Q(title__icontains=query) |
        Q(ingredients__icontains=query) |
        Q(tags__name__icontains=query) |
        Q(instructions__icontains=query)
    ).distinct()
    return recipes
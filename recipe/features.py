from recipe.models import Recipe,Tag
from django.db.models import Q
from recipe.models import UserFavourite,UserHistory
from ipware import get_client_ip


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

#is used to create or add to the user history
def create_or_add_to_history(request, recipe):
    if request.user.is_authenticated:
        user_history,created = UserHistory.objects.get_or_create(user=request.user)
        if not user_history.recipe.filter(pk=recipe.pk).exists():
            user_history.recipe.add(recipe)
    else:
        client_ip, is_routable = get_client_ip(request)
        user_history,created=UserHistory.objects.get_or_create(ip_address=client_ip)
        if not user_history.recipe.filter(pk=recipe.pk).exists():
            user_history.recipe.add(recipe)
from recipe.models import Recipe,Tag
from django.db.models import Q
from recipe.models import UserFavourite,UserHistory
from ipware import get_client_ip
from django import http

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
from django.core.exceptions import MultipleObjectsReturned

def create_or_add_to_history(request, recipe):
    if request.user.is_authenticated:
        try:
            user_history = UserHistory.objects.get(user=request.user)
        except UserHistory.DoesNotExist:
            user_history = UserHistory.objects.create(user=request.user)
        except MultipleObjectsReturned:
            user_history = UserHistory.objects.filter(user=request.user).first()
    else:
        client_ip, is_routable = get_client_ip(request)
        try:
            user_history = UserHistory.objects.get(ip_address=client_ip)
        except UserHistory.DoesNotExist:
            user_history = UserHistory.objects.create(ip_address=client_ip)
        except MultipleObjectsReturned:
            user_history = UserHistory.objects.filter(ip_address=client_ip).first()

    if not user_history.recipe.filter(pk=recipe.pk).exists():
        user_history.recipe.add(recipe)

    return user_history



#is used to add or remove recipe from user favourite
def add_or_remove_favourite(request,slug):
    '''
    Add or remove recipe from user favourite
    '''
    try:
        recipe = Recipe.objects.get(slug=slug)
        user_favourite,created=UserFavourite.objects.get_or_create(user=request.user)
    except Exception as e:
        return http.HttpResponseBadRequest()
    if recipe in user_favourite.recipe.all():
        user_favourite.recipe.remove(recipe)
    else:
        user_favourite.recipe.add(recipe)
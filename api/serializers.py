from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from recipe.models import Recipe,Tag

User=get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author=UserSerializer(read_only=True)
    class Meta:
        model = Recipe
        fields = ['title','author', 'recipe_image', 'tags', 'ingredients', 'servings', 'prep_time', 'instructions']

class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    custom_tags = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Recipe
        fields = ['title', 'recipe_image', 'tags', 'custom_tags', 'ingredients', 'servings', 'prep_time', 'instructions']


class RecipeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['title', 'recipe_image', 'tags', 'ingredients', 'servings', 'prep_time', 'instructions']



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username','email','password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
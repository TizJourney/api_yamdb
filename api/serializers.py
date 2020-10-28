from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
        model = User


class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class EmailAuthTokenInputSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class EmailAuthTokenOutputSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    
    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        model = models.Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    
    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        model = models.Comment

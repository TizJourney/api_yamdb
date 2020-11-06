from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Запрещено использовать имя me')

        if value.startswith(User.AUTO_CREATE_USERNAME_PREFIX):
            raise serializers.ValidationError(
                (
                    'Имя не должно начинаться с '
                    f'{User.AUTO_CREATE_USERNAME_PREFIX}'
                )
            )
        return value

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

# специальный сериализатор с ограничениями на изменение полей:
# нельзя менять роль
class RestrictedUserSerializer(UserSerializer):
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
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
    """
    Сериализатор для ReviewViewSet
    """
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate(self, data):
        """
        Валидация для проверки того,
        был ли уже создан отзыв пользователя
        на произведение
        """
        title_id = self.context.get('title_id')
        request = self.context.get('request')
        if (
            request.method != 'PATCH' and
            models.Review.objects.filter(
                author=request.user, title_id=title_id
            ).exists()
        ):
            raise serializers.ValidationError('Отзыв уже существует')
        return data

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
    """
    Сериализатор для CommentViewSet
    """
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

# !!!!!!не проходило тесты без этого
class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True, required=False, default=0)
    class Meta:
        fields = '__all__'
        model = models.Title
# !!!!!!не проходило тесты без этого

from django.contrib.auth import get_user_model
from rest_framework import serializers

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
            'is_active'
        )
        model = User

class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

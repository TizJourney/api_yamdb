from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'role')
        model = User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.models import User


# Сериализатор модели пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'created', 'updated', 'username', \
                 'fullname', 'user_type', 'date_joined', \
                 'password'


class TokenSerializer(serializers.ModelSerializer):
    user_item = UserSerializer(
        many=False,
        source='user',
        read_only=True,
    )

    class Meta:
        model = Token
        fields = 'key', 'user', 'user_item'

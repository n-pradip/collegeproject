from rest_framework import serializers
from .models import User, UserTokens

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserTokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTokens
        fields = ('user', 'password_reset_token')

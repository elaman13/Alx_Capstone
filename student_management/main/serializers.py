from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    """Serialize and create authenticated users token while deleting the previous if existed.
        """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    
    def create(self, validated_data): 
        """Authenticate and return a new token."""
        username = validated_data.get('username', None)
        password = validated_data.get('password', None)

        user = authenticate(username=username, password=password)
        print(f'user: {user}')
        
        if user is not None:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return {"username": username, "token": token.key}
        
        raise AuthenticationFailed('Username or Password not match.')
        

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
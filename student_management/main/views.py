from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from . import serializers

User = get_user_model()

# Create your views here.
class LoginView(generics.GenericAPIView):
    """
    Login View for post request only.
    """
    serializer_class = serializers.LoginSerializer
    queryset = User.objects.all()

    def post(self,request):
        """
        return username and token when users logs in.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()

        return Response(token, status=status.HTTP_200_OK)


class SignUpView(generics.GenericAPIView):
    """
    Register User
    """
    serializer_class = serializers.SignUpSerializer
    queryset = User.objects.all()

    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

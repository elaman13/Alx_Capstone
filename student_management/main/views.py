from rest_framework import generics, status
from rest_framework.response import Response
from . import models, serializers

# Create your views here.
class LoginView(generics.GenericAPIView):
    """
    Login View for post request only.
    """
    serializer_class = serializers.LoginSerializer

    def get(self, request):
        user = models.User.objects.get(pk=request.user.id)

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response(token, status=status.HTTP_200_OK)


class SignUpView(generics.GenericAPIView):
    serializer_class = serializers.SignUpSerializer
    queryset = models.User.objects.all()

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

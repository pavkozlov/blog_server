from rest_framework import views, response, status, generics
from apps.authorization.serializers import RegistrationSerializer, ProfileSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class RegistrationView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'patch', 'post', 'delete']
    queryset = get_user_model().objects.all()
    serializer_class = ProfileSerializer


class LoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_user_model().objects.filter(email=request.data['email'])
        if user.exists() and user.first().check_password(request.data['password']):
            token,_ = Token.objects.get_or_create(user=user.first())
            return response.Response(token.key)

        return response.Response('Проверьте логин/пароль', status=status.HTTP_400_BAD_REQUEST)

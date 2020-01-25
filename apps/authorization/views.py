from rest_framework import views, response, status, generics
from apps.authorization.serializers import RegistrationSerializer, ProfileSerializer
from django.contrib.auth import get_user_model


class RegistrationView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileSerializer

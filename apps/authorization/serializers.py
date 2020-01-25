from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, max_length=20)

    def validate_email(self, value):
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("Такой email уже существует")
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(max_length=20, required=False, write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, *args, **kwargs):
        token, _ = Token.objects.get_or_create(user=self.instance)
        return token.key

    def validate_email(self, value):
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("Такой email уже существует")
        return value

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            password = validated_data.pop('password')
            profile = super(ProfileSerializer, self).update(instance, validated_data)
            profile.set_password(password)
            profile.save()
            return profile
        return super(ProfileSerializer, self).update(instance, validated_data)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'last_login', 'is_superuser', 'first_name', 'last_name', 'date_joined', 'password',
                  'token']

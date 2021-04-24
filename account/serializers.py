from django.contrib.auth import authenticate
from rest_framework import serializers

from account.models import MyUser
from rest_framework.pagination import PageNumberPagination
from account.utils import send_activation_email


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirmation = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirmation')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirmation = validated_data.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Пароли не совпадают.')
        return validated_data

    def create(self, validated_data):

        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_activation_email(email=user.email, activation_code=user.activation_code, is_password=False)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                message = 'Невозможно войти в систему с предоставленными учетными данными.'
                raise serializers.ValidationError(message, code='authorization')

        else:
            message = 'Нужно ввести "электронную почту" и "пароль".'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(min_length=20)
    password = serializers.CharField(min_length=6, required=True)
    password_confirmation = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с данным адресом электронной почты не существует')
        return email

    def validate_activation_code(self, code):
        if not MyUser.objects.filter(activation_code=code, is_active=False).exists():
            raise serializers.ValidationError('Неправильный активационный код.')
        return code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Пароли не совпадают.')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        code = data.get('activation_code')
        password = data.get('password')
        try:
            user = MyUser.objects.get( email=email, activation_code=code, is_active=False)
        except:
            raise serializers.ValidationError('User not found')
        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
        return user


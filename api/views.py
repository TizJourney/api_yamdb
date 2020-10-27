from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, decorators
from .serializers import (
    UserSerializer,
    EmailAuthSerializer,
    EmailAuthTokenInputSerializer,
    EmailAuthTokenOutputSerializer,
)
from django.core.mail import send_mail
from rest_framework import response, status
from django.views.decorators.csrf import csrf_exempt
from smtplib import SMTPException
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

token_generator = PasswordResetTokenGenerator()


def _get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class UsersViewSet(viewsets.ModelViewSet):
    # пользователи доложны сначала пройти актавацию через e-mail
    # прежде, чем будут признаны настоящими
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer


@csrf_exempt
@decorators.api_view(['POST'])
def auth_send_email(request):
    input_data = EmailAuthSerializer(data=request.data)
    if not input_data.is_valid():
        return response.Response(
            input_data.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    email = input_data.validated_data['email']

    user_object, created = User.objects.get_or_create(email=email)

    if created:
        user_object.is_active = False
        user_object.save()

    confirmation_code = token_generator.make_token(user_object)

    try:
        send_mail(
            'Получение доступа к социальной сети YamDB',
            f'Ваш код активации: {confirmation_code}',
            None, # from: использовать DEFAULT_FROM_EMAIL
            [email],
            fail_silently=False,
        )
    except SMTPException as e:
        return response.Response(
            f'Ошибка посылки e-mail: {e}',
            status=status.HTTP_400_BAD_REQUEST
        )

    return response.Response(input_data.data, status=status.HTTP_200_OK)


@csrf_exempt
@decorators.api_view(['POST'])
def auth_get_token(request):
    input_data = EmailAuthTokenInputSerializer(data=request.data)
    if not input_data.is_valid():
        return response.Response(
            input_data.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    email = input_data.validated_data['email']
    confirmation_code = input_data.validated_data['confirmation_code']

    user_object = get_object_or_404(User, email=email)

    if not token_generator.check_token(user_object, confirmation_code):
        return response.Response(
            f'Неверный код подтверждения',
            status=status.HTTP_400_BAD_REQUEST
        )

    token = _get_token_for_user(user_object)

    output_data = EmailAuthTokenOutputSerializer(data={'token': token})
    if not output_data.is_valid():
        return response.Response(
            output_data.errors,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response.Response(output_data.data, status=status.HTTP_200_OK)

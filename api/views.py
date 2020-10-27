from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, decorators
from .serializers import UserSerializer, EmailAuthSerializer
from django.core.mail import send_mail
from rest_framework import response, status
from django.views.decorators.csrf import csrf_exempt
from smtplib import SMTPException

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    # пользователи доложны сначала пройти актавацию через e-mail
    # прежде, чем будут признаны настоящими
    # queryset = User.objects.filter(is_active=True)
    queryset = User.objects.all()
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

    confirmation_code = 0

    try:
        send_mail(
            'Получение доступа к социальной сети YamDB',
            f'Ваш код активации {0}',
            None,
            [email],
            fail_silently=False,
        )
    except SMTPException as e:
        return response.Response(
            f'Ошибка посылки e-mail: {e}',
            status=status.HTTP_400_BAD_REQUEST
        )

    return response.Response(status=status.HTTP_200_OK)

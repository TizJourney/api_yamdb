from smtplib import SMTPException

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (decorators, filters, permissions, response, status,
                            viewsets, generics)
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Comment, Genre, Review, Title
from .permissions import AdminOnly, AdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateTitleSerializer, EmailAuthSerializer,
                          EmailAuthTokenInputSerializer,
                          EmailAuthTokenOutputSerializer, GenreSerializer,
                          RestrictedUserSerializer, ReviewSerializer,
                          TitleSerializer, UserSerializer)

User = get_user_model()

token_generator = PasswordResetTokenGenerator()


def _get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class UsersViewSet(viewsets.ModelViewSet):
    # is_active: пользователи должны сначала пройти активацию через e-mail
    # прежде, чем получат доступ в социальную сеть
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, AdminOnly]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = (['username'])

    @decorators.action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request, pk=None):
        user_object = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = UserSerializer(user_object)
            return response.Response(serializer.data)
        # PATCH
        serializer = RestrictedUserSerializer(
            user_object,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return response.Response(serializer.data)


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
            None,  # from: использовать DEFAULT_FROM_EMAIL
            [email],
            fail_silently=False,
        )
    except SMTPException as e:
        return response.Response(
            f'Ошибка посылки e-mail: {e}',
            status=status.HTTP_400_BAD_REQUEST
        )

    return response.Response(input_data.data, status=status.HTTP_200_OK)


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

    if not user_object.is_active:
        user_object.is_active = True
        user_object.save()

    token = _get_token_for_user(user_object)

    output_data = EmailAuthTokenOutputSerializer(data={'token': token})
    return response.Response(output_data.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user,
            review=review
        )


class GenreViewSet(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)
    lookup_field = "slug"


class CategoryViewSet(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ("category", "genre")
    search_fields = ("name", "year")

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTitleSerializer
        return TitleSerializer

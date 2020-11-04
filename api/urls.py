from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

router = DefaultRouter()
router.register(r'users', views.UsersViewSet)
router.register(r'titles', views.TitleViewSet, basename='titles')
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'genres', views.GenreViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename="reviews"
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename="comments"
)

v1_url_patterns = [
    path('auth/mail/', views.auth_send_email, name='auth_send_mail'),
    path('auth/token/', views.auth_get_token, name='auth_get_token'),
]

urlpatterns = [
    path('v1/', include(v1_url_patterns)),
    path('v1/', include(router.urls)),
    # path('v1/genres/', views.GenreViewSet.as_view()),
    # path('v1/categories/', views.CategoryViewSet.as_view()),
]

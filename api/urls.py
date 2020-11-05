from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', views.UsersViewSet)
router.register(r'titles', views.TitleViewSet) # !!!!!!не проходило тесты без этого
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
]

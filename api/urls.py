from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UsersViewSet)
router.register(r'titles', views.TitleViewSet, basename='titles')
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'genres', views.GenreViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

auth_url_patterns = [
    path('mail/', views.auth_send_email, name='auth_send_mail'),
    path('token/', views.auth_get_token, name='auth_get_token'),
]


v1_url_patterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_url_patterns)),
]

urlpatterns = [
    path('v1/', include(v1_url_patterns)),
]

from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

v1_url_patterns = [
    # это заглушки для проверки правильности подключения jwt-токенов. Ближайшее время будут убраны.
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('v1/', include(v1_url_patterns)),
]

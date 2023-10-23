from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import (
    UserRegistrationView,
    ChangePasswordView
)


urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/register/', UserRegistrationView.as_view(),),
    path('auth/change-password/', ChangePasswordView.as_view(),),
]

from django.urls import path
from .views import RegisterView, VerifyEmailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('password-reset/', reset_password_request_token, name='password-reset'),
    path('password-reset/confirm/', reset_password_confirm, name='password-reset-confirm'),
]

# /api/users/password-reset/ with email. It sends a token via email (printed in console for now)
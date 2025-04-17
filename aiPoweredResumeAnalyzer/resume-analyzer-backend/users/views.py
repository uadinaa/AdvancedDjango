from rest_framework import generics
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.urls import reverse
from .utils import email_verification_token
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin
from django.core.mail import send_mail

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


def send_verification_email(user, request):
    try:
        token = email_verification_token.make_token(user)
        uid = user.pk
        verification_link = request.build_absolute_uri(
            reverse('verify-email') + f'?uid={uid}&token={token}'
        )
        print(f"Verification link: {verification_link}")

        send_mail(
            'Verify your email',
            f'Click the link to verify your account: {verification_link}',
            'no-reply@resumanalyzer.com',
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error in sending verification email: {e}")




class VerifyEmailView(APIView):
    def get(self, request):
        uid = request.GET.get('uid')
        token = request.GET.get('token')

        try:
            user = User.objects.get(pk=uid)
            if email_verification_token.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({'message': 'Email verified successfully!'})
            else:
                return Response({'error': 'Invalid token'}, status=400)
        except User.DoesNotExist:
            return Response({'error': 'Invalid user'}, status=400)


class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = CustomUser.objects.all()
        user_data = [{"email": user.email, "role": user.role} for user in users]
        return Response(user_data)



def send_verification_email(user, request):
    token = email_verification_token.make_token(user)
    uid = user.pk
    verification_link = request.build_absolute_uri(
        reverse('verify-email') + f'?uid={uid}&token={token}'
    )

    print(f"Sending email with link: {verification_link}")  # For debugging

    send_mail(
        'Verify your email',
        f'Click the link to verify your account: {verification_link}',
        'no-reply@resumanalyzer.com',
        [user.email],
        fail_silently=False,
    )

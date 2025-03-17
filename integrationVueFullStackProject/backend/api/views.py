from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Item
from .serializers import ItemSerializer, UserSerializer, RegisterSerializer
from .permissions import IsAdmin
from rest_framework.permissions import AllowAny

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
#
#     def get_permissions(self):
#         if self.request.method in ['POST', 'PUT', 'DELETE']:
#             return [IsAuthenticated(), IsAdmin()]
#         return [IsAuthenticated()]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]  # Allow everyone to access


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
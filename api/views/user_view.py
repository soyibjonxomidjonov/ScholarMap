from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers import UserSerializerConfig
from api.models import User
from rest_framework import viewsets
from rest_framework import filters
from api.permissions import IsOwnerOrReadOnly







class CustomPagination(PageNumberPagination):
    page_size = 3




class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializerConfig
    pagination_class = CustomPagination

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.filters import UserFilter
from api.serializers import UserSerializerConfig
from api.models import User
from rest_framework import viewsets
from rest_framework import filters
from api.permissions import IsOwnerOrReadOnly
from django_filters import rest_framework as django_filters







class CustomPagination(PageNumberPagination):
    page_size = 3




class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializerConfig
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = UserFilter
    search_fields = ['university', 'eslatma_matni', 'qolgan_kun', 'tugash_kun']
    pagination_class = CustomPagination

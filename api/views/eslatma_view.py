from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.filters import EslatmaFilter
from api.serializers import EslatmaSerializerConfig
from api.models import Eslatma
from rest_framework import viewsets

from rest_framework import filters
from django_filters import rest_framework as django_filters


class CustomPagination(PageNumberPagination):
    page_size = 20




class EslatmaViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Eslatma.objects.all()
    serializer_class = EslatmaSerializerConfig
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = EslatmaFilter
    search_fields = ['university', 'eslatma_matni', 'qolgan_kun', 'tugash_kun']
    pagination_class = CustomPagination

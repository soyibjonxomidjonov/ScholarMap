from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.filters import UniversityFilter
from api.serializers import UniversitySerializerConfig
from api.models import University
from rest_framework import viewsets

from django_filters import rest_framework as django_filters
from rest_framework import filters







class CustomPagination(PageNumberPagination):
    page_size = 20




class UniversitetViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = University.objects.all()
    serializer_class = UniversitySerializerConfig
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = UniversityFilter
    search_fields = ['university_name', 'state', 'grant_name']
    pagination_class = CustomPagination

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers import UniversitySerializerConfig
from api.models import University
from rest_framework import viewsets








class CustomPagination(PageNumberPagination):
    page_size = 3




class UniversitetViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = University.objects.all()
    serializer_class = UniversitySerializerConfig
    pagination_class = CustomPagination
    swagger_tags = ['1. Users']

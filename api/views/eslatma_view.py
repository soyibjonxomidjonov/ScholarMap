from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers import EslatmaSerializerConfig
from api.models import Eslatma
from rest_framework import viewsets








class CustomPagination(PageNumberPagination):
    page_size = 20




class EslatmaViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Eslatma.objects.all()
    serializer_class = EslatmaSerializerConfig
    pagination_class = CustomPagination

from drf_yasg.openapi import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from api.serializers import TranslateSerializerConfig












@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication]) # bunda belgilab qoyildi
@parser_classes([MultiPartParser, FormParser]) # Fayllar bilan ishlash uchun shart
@permission_classes([IsAuthenticated]) # Bunda permison qoshildi
def product_list(request):
    serializer = TranslateSerializerConfig(data=request.data)

    if serializer.is_valid():
        target_lang = serializer.validated_data['target_lang']
        text = serializer.validated_data.get('text')
        file = serializer.validated_data.get('file')




    return Response(serializer.data)



















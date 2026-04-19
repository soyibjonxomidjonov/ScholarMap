from drf_yasg.utils import swagger_auto_schema # 1. Buni import qiling
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.serializers import TranslateSerializerConfig # Serializeriz

@swagger_auto_schema(
    method='post',
    request_body=TranslateSerializerConfig, # 2. Mana bu qator Swaggerga "shu maydonlarni ko'rsat" deydi
    response={201: TranslateSerializerConfig}
)
@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def your_functional_view(request):
    serializer = TranslateSerializerConfig(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=201)
    return Response(serializer.errors, status=400)
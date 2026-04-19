from django.http import JsonResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from api.serializers import TranslateSerializerConfig


from api.services.translate import translate_text
from api.services.AI import AI_translate_image, AI_image_chat, AI_chat
from api.services.misc import text_to_pdf

from drf_spectacular.utils import extend_schema # 1. Importni qo'shi




# @permission_classes([IsAuthenticated]) # Bunda permison qoshildi
# @authentication_classes([SessionAuthentication, BasicAuthentication]) # bunda belgilab qoyildi


#
@swagger_auto_schema(
    method='post',
    request_body=TranslateSerializerConfig, # 2. Mana bu qator Swaggerga "shu maydonlarni ko'rsat" deydi
    response={201: TranslateSerializerConfig}
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser]) # Fayllar bilan ishlash uchun shart
def super_ai_translate(request):
    serializer = TranslateSerializerConfig(data=request.data)
    serializer.is_valid(raise_exception=True) # Xatolarni avtomatik qaytaradi

    if serializer.is_valid():
        target_lang = serializer.validated_data['target_lang']
        text = serializer.validated_data.get('text')
        file = serializer.validated_data.get('file')
        response_type = serializer.validated_data.get('response_type', 'text')

        if target_lang != None and file != None:
            translation = AI_translate_image(text, file, target_lang)
            print(f"DEBUG translation: {translation}")  # ← shu qatorni qo'shing
            if response_type == "pdf":
                if isinstance(translation, dict):
                    text_to_print = translation.get('translated_text', '')
                else:
                    text_to_print = translation
                pdf_response = text_to_pdf(text_to_print)
                response = HttpResponse(pdf_response, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="translation.pdf"'
                return response
            return Response(translation)

        else:
            translation = translate_text(text, target_lang)
            if response_type == "pdf":
                print(f"DEBUG: Translation qiymati: {translation}")
                print(f"DEBUG: Translation turi: {type(translation)}")

                if isinstance(translation, dict):
                    # 'translated_text' kalitini ishlating, chunki logingizda aynan shu nomdagi kalit bor
                    text_to_print = translation.get('translated_text')
                else:
                    text_to_print = translation

                # Endi tekshirish uchun buni ham qo'shib qo'ying:
                if text_to_print is None:
                    text_to_print = "Matn topilmadi"
                print(text_to_print)
                print(f"Qatorlar soni: {len(translation.get('translated_text', '').split(chr(10)))}")
                pdf_response = text_to_pdf(text_to_print)


                response = HttpResponse(pdf_response, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="translation.pdf"'
                return response
            return Response(translation)


    return JsonResponse({"message": "Noto'g'ri ma'lumotlar kiritildi", "errors": serializer.errors}, status=400)
#





# @authentication_classes([SessionAuthentication, BasicAuthentication]) # bunda belgilab qoyildi
# @permission_classes([IsAuthenticated]) # Bunda permison qoshildi


@swagger_auto_schema(
    method='post',
    request_body=TranslateSerializerConfig, # 2. Mana bu qator Swaggerga "shu maydonlarni ko'rsat" deydi
    response={201: TranslateSerializerConfig}
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser]) # Fayllar bilan ishlash uchun shart
def ai_chat(request):
    serializer = TranslateSerializerConfig(data=request.data)

    serializer.is_valid(raise_exception=True) # Xatolarni avtomatik qaytaradi
    text = serializer.validated_data.get('text')
    file = serializer.validated_data.get('file')
    response_type = serializer.validated_data.get('response_type', 'text')

    if not text and not file:
        return JsonResponse({"message": "Matn yoki fayl kiritilishi kerak"}, status=400)

    if file:
        if response_type == "pdf":
            response = AI_image_chat(text, file)
            pdf_response = text_to_pdf(response)
            http_response = HttpResponse(pdf_response, content_type='application/pdf')
            http_response['Content-D    isposition'] = 'attachment; filename="chat_response.pdf"'
            return http_response
        response = AI_image_chat(text, file)
        return Response(response)
    else:
        if response_type == "pdf":
            response = AI_chat(text)
            pdf_response = text_to_pdf(response)
            http_response = HttpResponse(pdf_response, content_type='application/pdf')
            http_response['Content-Disposition'] = 'attachment; filename="chat_response.pdf"'
            return http_response
        response = AI_chat(text)
        return Response(response)
















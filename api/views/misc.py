from django.http import JsonResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import TranslateSerializerConfig


from api.services.translate import translate_text
from api.services.AI import AI_translate_image, AI_image_chat, AI_chat, AI_translate_text
from api.services.misc import text_to_pdf
from api.services.document_parser import extract_text_from_file

from drf_spectacular.utils import extend_schema # 1. Importni qo'shi

from api.tasks import ai_chat_task
from celery.result import AsyncResult


@swagger_auto_schema(
    method='post',
    request_body=TranslateSerializerConfig, # 2. Mana bu qator Swaggerga "shu maydonlarni ko'rsat" deydi
    response={201: TranslateSerializerConfig}
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
            file_ext = file.name.lower().split('.')[-1] if file.name else ''
            
            if file_ext in ['pdf', 'docx']:
                extracted_text = extract_text_from_file(file, file.name)
                full_text = f"{text}\n\n{extracted_text}" if text else extracted_text

                translation_result = AI_translate_text(full_text, target_lang)
                translation = {"detected_lang": "auto", "translated_text": translation_result}
            else:
                translation = AI_translate_image(text, file, target_lang)

            if response_type == "pdf":
                if isinstance(translation, dict):
                    text_to_print = translation.get('translated_text', '')
                else:
                    text_to_print = translation
                pdf_response = text_to_pdf(text_to_print)
                response = HttpResponse(pdf_response, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="translation.pdf"'
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                return response
            return Response(translation)

        else:
            translation = translate_text(text, target_lang)
            if response_type == "pdf":
                if isinstance(translation, dict):
                    text_to_print = translation.get('translated_text')
                else:
                    text_to_print = translation

                if text_to_print is None:
                    text_to_print = "Matn topilmadi"

                pdf_response = text_to_pdf(text_to_print)
                response = HttpResponse(pdf_response, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="translation.pdf"'
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                return response
            return Response(translation)


    return JsonResponse({"message": "Noto'g'ri ma'lumotlar kiritildi", "errors": serializer.errors}, status=400)
#





@swagger_auto_schema(
    method='post',
    request_body=TranslateSerializerConfig, # 2. Mana bu qator Swaggerga "shu maydonlarni ko'rsat" deydi
    response={201: TranslateSerializerConfig}
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
        file_ext = file.name.lower().split('.')[-1] if file.name else ''
        
        if file_ext in ['pdf', 'docx']:
            extracted_text = extract_text_from_file(file, file.name)
            full_text = f"{text}\n\n{extracted_text}" if text else extracted_text
            
            if response_type == "pdf":
                response = AI_chat(full_text)
                pdf_response = text_to_pdf(response)
                http_response = HttpResponse(pdf_response, content_type='application/pdf')
                http_response['Content-Disposition'] = 'attachment; filename="chat_response.pdf"'
                http_response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                return http_response
            
            response = AI_chat(full_text)
            return Response(response)
        else:
            if response_type == "pdf":
                response = AI_image_chat(text, file)
                pdf_response = text_to_pdf(response)
                http_response = HttpResponse(pdf_response, content_type='application/pdf')
                http_response['Content-Disposition'] = 'attachment; filename="chat_response.pdf"'
                http_response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                return http_response
            response = AI_image_chat(text, file)
            return Response(response)
    else:
        if response_type == "pdf":
            response = AI_chat(text)
            pdf_response = text_to_pdf(response)
            http_response = HttpResponse(pdf_response, content_type='application/pdf')
            http_response['Content-Disposition'] = 'attachment; filename="chat_response.pdf"'
            http_response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return http_response
        task = ai_chat_task.delay(text)
        return Response({"task_id": task.id, "status": "processing"})







@api_view(['GET'])
def ai_chat_result(request, task_id):
    task = AsyncResult(task_id)
    if task.ready():
        return Response({"status": "completed", "result": task.result})
    return Response({"status": "processing"})








"""
Chatbot API Views — Groq + LangChain
--------------------------------------
POST   /api/v1/chatbot/          — Chatbot'ga xabar yuborish (suhbat)
DELETE /api/v1/chatbot/clear/    — Suhbat tarixini tozalash
GET    /api/v1/chatbot/history/  — Joriy suhbat tarixini ko'rish
"""
import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, parser_classes
)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import University
from api.services.chatbot import (
    chatbot_respond,
    chatbot_clear_history,
    get_history_messages,
)

logger = logging.getLogger(__name__)


# ─── Serializer ───────────────────────────────────────────────────────────────
class ChatbotMessageSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=5000,
        help_text="Foydalanuvchining savoli yoki xabari."
    )
    include_universities = serializers.BooleanField(
        required=False,
        default=True,
        help_text="True bo'lsa (defolt), chatbot bazadagi universitetlarni ko'radi."
    )


# ─── 1. CHATBOT XABAR YUBORISH ────────────────────────────────────────────────

@swagger_auto_schema(
    method='post',
    request_body=ChatbotMessageSerializer,
    responses={
        200: openapi.Response(
            description="Chatbot javobi",
            examples={
                "application/json": {
                    "success": True,
                    "reply": "Salom! Kompyuter fanlari bo'yicha Germaniyada...",
                    "session_id": "user_42"
                }
            }
        ),
        400: openapi.Response(description="Noto'g'ri so'rov"),
        500: openapi.Response(description="AI xatosi yoki konfiguratsiya xatosi"),
    },
    operation_summary="ScholarMap AI Chatbot (Groq + LangChain)",
    operation_description=(
        "Groq LLM (Llama-3.3-70b) + LangChain yordamida ishlaydi.\n\n"
        "Chatbot quyidagilarni qiladi:\n"
        "- Bazadagi universitetlar va grantlar haqida savollarga javob beradi\n"
        "- Foydalanuvchi profiliga mos universitetlarni tavsiya qiladi\n"
        "- Suhbat tarixini avtomatik saqlaydi (foydalanuvchi IDsi asosida)\n\n"
        "Har bir foydalanuvchi o'z alohida sessiyasiga ega.\n"
        "Yangi suhbat boshlash uchun DELETE /api/v1/chatbot/clear/ ga murojaat qiling."
    )
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def chatbot_message(request):
    serializer = ChatbotMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(
            {
                "success": False,
                "error": {"code": "VALIDATION_ERROR", "message": serializer.errors}
            },
            status=400
        )

    user_message = serializer.validated_data['message']
    include_universities = serializer.validated_data.get('include_universities', True)

    # Foydalanuvchi IDsi asosida unikal session
    session_id = f"user_{request.user.id}"

    # Universitetlarni DB'dan olish
    universities_data = []
    if include_universities:
        universities_data = list(
            University.objects.values(
                'university_name', 'state', 'level',
                'grant_name', 'grand_amount', 'grand_turi',
                'directions', 'reception_start', 'reception_end'
            )
        )

    try:
        reply = chatbot_respond(
            session_id=session_id,
            user_message=user_message,
            universities_data=universities_data,
        )
        return Response({
            "success": True,
            "reply": reply,
            "session_id": session_id,
        })

    except RuntimeError as e:
        logger.error(f"Chatbot konfiguratsiya xatosi: {e}")
        return JsonResponse(
            {
                "success": False,
                "error": {"code": "CONFIG_ERROR", "message": str(e)}
            },
            status=500
        )
    except Exception as e:
        logger.exception("Chatbot kutilmagan xatolik")
        return JsonResponse(
            {
                "success": False,
                "error": {
                    "code": "AI_ERROR",
                    "message": "AI javob berishda xatolik yuz berdi. Keyinroq urinib ko'ring."
                }
            },
            status=500
        )


# ─── 2. SUHBAT TARIXINI TOZALASH ─────────────────────────────────────────────

@swagger_auto_schema(
    method='delete',
    responses={
        200: openapi.Response(
            description="Suhbat tarixi tozalandi",
            examples={"application/json": {"success": True, "message": "Yangi suhbat boshlandi."}}
        ),
    },
    operation_summary="Chatbot suhbat tarixini tozalash",
    operation_description="Foydalanuvchining joriy sessiyasini o'chirib, yangi suhbat boshlaydi."
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def chatbot_clear(request):
    session_id = f"user_{request.user.id}"
    chatbot_clear_history(session_id)
    return Response({"success": True, "message": "Yangi suhbat boshlandi."})


# ─── 3. SUHBAT TARIXINI KO'RISH ──────────────────────────────────────────────

@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="Suhbat tarixi",
            examples={
                "application/json": {
                    "success": True,
                    "history": [
                        {"role": "user", "content": "Salom"},
                        {"role": "assistant", "content": "Salom! Qanday yordam bera olaman?"}
                    ],
                    "total": 2
                }
            }
        ),
    },
    operation_summary="Chatbot suhbat tarixini ko'rish",
    operation_description="Foydalanuvchining joriy sessiyasidagi barcha xabarlarni qaytaradi."
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def chatbot_history(request):
    session_id = f"user_{request.user.id}"
    messages = get_history_messages(session_id)
    return Response({
        "success": True,
        "history": messages,
        "total": len(messages),
    })

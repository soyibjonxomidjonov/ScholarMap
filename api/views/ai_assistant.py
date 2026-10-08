"""
AI Assistant & University Matching Views
-----------------------------------------
POST /api/v1/ai-assistant/          — Suhbat (chat with universities context)
POST /api/v1/ai-find-universities/  — Profil bo'yicha mos universitetlarni topish
"""
import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, parser_classes
)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import AssistantSerializer, UniversityMatchSerializer
from api.models import University
from api.services.AI import AI_assistant, AI_find_universities

logger = logging.getLogger(__name__)


# ─── 1. AI SUHBAT (Chat) ──────────────────────────────────────────────────────

@swagger_auto_schema(
    method='post',
    request_body=AssistantSerializer,
    responses={
        200: openapi.Response(
            description="AI javobi",
            examples={"application/json": {"reply": "Salom! Qanday yordam bera olaman?"}}
        ),
        400: "Noto'g'ri so'rov",
        500: "Server xatosi",
    },
    operation_summary="ScholarMap AI Yordamchisi",
    operation_description=(
        "Foydalanuvchi bilan suhbat olib boradi. "
        "with_universities=true bo'lsa, AI bazadagi universitetlarni ko'rgan holda javob beradi. "
        "chat_history — frontend tomonidan saqlanib, har so'rovda yuborilishi kerak."
    )
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def ai_assistant_chat(request):
    serializer = AssistantSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(
            {"success": False, "error": {"code": "VALIDATION_ERROR", "message": serializer.errors}},
            status=400
        )

    data = serializer.validated_data
    user_message = data['message']
    chat_history = data.get('chat_history', [])
    with_universities = data.get('with_universities', False)

    universities_data = None
    if with_universities:
        unis = University.objects.values(
            'university_name', 'state', 'level', 'grant_name',
            'grand_amount', 'grand_turi', 'directions',
            'reception_start', 'reception_end'
        )
        universities_data = list(unis)

    try:
        reply = AI_assistant(
            user_message=user_message,
            chat_history=chat_history,
            universities_data=universities_data
        )
        return Response({"success": True, "reply": reply})
    except Exception as e:
        logger.exception("AI assistant xatosi")
        return JsonResponse(
            {"success": False, "error": {"code": "AI_ERROR", "message": str(e)}},
            status=500
        )


# ─── 2. UNIVERSITETLARNI TOPISH ───────────────────────────────────────────────

@swagger_auto_schema(
    method='post',
    request_body=UniversityMatchSerializer,
    responses={
        200: openapi.Response(
            description="AI tavsiyalari",
            examples={
                "application/json": {
                    "success": True,
                    "recommendations": "1. MIT — texnologiya yo'nalishi uchun eng mos...",
                    "matched_count": 5
                }
            }
        ),
        400: "Noto'g'ri so'rov",
        404: "Tizimda universitetlar yo'q",
    },
    operation_summary="Profil bo'yicha mos universitetlarni topish",
    operation_description=(
        "Foydalanuvchi yo'nalishi, darajasi, mamlakati va boshqa ma'lumotlari asosida "
        "bazadan eng mos 5 universitetni AI yordamida tavsiya qiladi."
    )
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def ai_find_universities(request):
    serializer = UniversityMatchSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(
            {"success": False, "error": {"code": "VALIDATION_ERROR", "message": serializer.errors}},
            status=400
        )

    # Bazadan barcha universitetlarni olish
    universities_qs = University.objects.values(
        'university_name', 'state', 'level', 'grant_name',
        'grand_amount', 'grand_turi', 'directions',
        'reception_start', 'reception_end'
    )
    universities_data = list(universities_qs)

    if not universities_data:
        return JsonResponse(
            {
                "success": False,
                "error": {
                    "code": "NO_UNIVERSITIES",
                    "message": "Hozircha tizimda universitetlar mavjud emas."
                }
            },
            status=404
        )

    user_profile = {
        k: str(v) for k, v in serializer.validated_data.items() if v
    }

    try:
        recommendations = AI_find_universities(
            user_profile=user_profile,
            universities_data=universities_data
        )
        return Response({
            "success": True,
            "recommendations": recommendations,
            "matched_count": len(universities_data),
        })
    except Exception as e:
        logger.exception("AI university matching xatosi")
        return JsonResponse(
            {"success": False, "error": {"code": "AI_ERROR", "message": str(e)}},
            status=500
        )

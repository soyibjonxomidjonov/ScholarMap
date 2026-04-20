import os

import requests
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.filters import EslatmaFilter
from api.serializers import EslatmaSerializerConfig
from api.models import Eslatma
from rest_framework import viewsets

from rest_framework import filters
from django_filters import rest_framework as django_filters




from celery import shared_task
from django.core.mail import send_mail






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




@shared_task
def send_eslatma_email(eslatma_id):
    try:
        eslatma = Eslatma.objects.get(pk=eslatma_id)
        message =f" Eslatma: {eslatma.eslatma_matni}\n" \
                 f"Qolgan kun: {eslatma.qolgan_kun}\n" \
                 f"Tugash kun: {eslatma.tugash_kun}\n" \
                 f"Universitet: {eslatma.universitet}\n"

        send_mail(
            subject="Eslatma",
            message=message,
            from_email=os.environ.get("EMAIL_HOST_USER"),  # Sizning email manzilingiz
            recipient_list=[eslatma.user.email],  # Eslatmani oluvchi email manzili
            fail_silently=False,
        )
    except Eslatma.DoesNotExist:
        return f"Eslatma ID: {eslatma_id} topilmadi."


@shared_task
def send_telegram_bot(eslatma_id, chat_id):
    try:
        eslatma = Eslatma.objects.get(pk=eslatma_id)
        message =f" Eslatma: {eslatma.eslatma_matni}\n" \
                 f"Qolgan kun: {eslatma.qolgan_kun}\n" \
                 f"Tugash kun: {eslatma.tugash_kun}\n" \
                 f"Universitet: {eslatma.universitet}\n"
        # Telegram bot API orqali xabar yuborish logikasi
        bot_token = os.environ.get("BOT_TOKEN")  # Telegram bot tokenini oling
        method = 'sendMessage'

        try:
            response = requests.post(
                url=f"https://api.telegram.org/bot{bot_token}/{method}",
                data={
                    "chat_id": chat_id,
                    "text": message
                },
                timeout=10
            ).json()
            res_data = response
            print(f"Telegram javobi: {res_data}")  # Nima bo'layotganini ko'rish uchun
            if not res_data.get('ok'):
                print(f"Telegram yubormadi: {res_data.get('description')}")
        except Exception as e:
            print(f'Xatolik {e}')

    except Eslatma.DoesNotExist:
        return f"Eslatma ID: {eslatma_id} topilmadi."
from celery import shared_task
from datetime import date
from api.models import Eslatma
from api.views.eslatma_view import send_eslatma_email, send_telegram_bot


from api.services.AI import AI_chat, AI_image_chat


@shared_task
def check_eslatmalar():
    bugun = date.today()
    eslatmalar = Eslatma.objects.filter(eslatma_kun=bugun)

    for eslatma in eslatmalar:
        if eslatma.eslatma_kun == bugun:
            if eslatma.ogohlantirish_sms == "gmail":
                send_eslatma_email.delay(eslatma.id)
            elif eslatma.ogohlantirish_sms == "bot":
                send_telegram_bot.delay(eslatma.id, eslatma.chat_id)
    return f"{eslatmalar.count()} ta eslatma yuborildi."

# Sinov


@shared_task
def ai_chat_task(text, file_path=None):
    if file_path:
        return AI_image_chat(text, file_path)
    return AI_chat(text)
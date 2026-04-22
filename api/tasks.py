from celery import shared_task
from datetime import date
from api.models import Eslatma
from api.views.eslatma_view import send_eslatma_email, send_telegram_bot


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



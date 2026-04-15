from django.db import models
from .user import User
from django.utils import timezone
from .universities import University

warning_sms = (
    ("gmail", "Gmail"),
    ("bot", "Bot"),
)


class Eslatma(models.Model):
    eslatma_matni = models.CharField(max_length=300, blank=False, null= False)
    universitet = models.ForeignKey(University, on_delete=models.CASCADE, related_name='eslatma_universitet')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="eslatma_user")

    ogohlantirish_sms = models.CharField(max_length=300,
                                         default="gmail"
                                         ,blank=True,
                                         choices=warning_sms
                                         ,null= True, verbose_name="Ogohlantirish SMS matni")
    eslatma_kun = models.DateField(blank=True, null= True, verbose_name="Eslatish sanasi")
    chat_id = models.CharField(max_length=300, blank=True, null=True, verbose_name="Telegram chat ID")
    @property
    def qolgan_kun(self):
        bugun = timezone.now().date()
        qabul_kuni = self.universitet.reception_start

        if qabul_kuni > bugun:
            qolgan_kun = qabul_kuni - bugun
            return qolgan_kun.days
        return 0
    @property
    def tugash_kun(self):
        bugun = timezone.now().date()
        tugash_kuni = self.universitet.reception_end

        if tugash_kuni > bugun:
            tugash_kun = tugash_kuni - bugun
            return tugash_kun.days
        return 0


    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
from django.db import models
from .user import User
from django.utils import timezone


class University(models.Model):
    university_name = models.CharField(max_length=100, blank=False, null= False)
    state = models.CharField(max_length=100, blank=False, null= False)

    level = models.CharField(max_length=50, blank=False, null= False)
    grant_name = models.CharField(max_length=100, blank=False, null= False)

    grand_amount = models.CharField(max_length=100 ,blank=False, null= False)
    grand_turi = models.CharField(max_length=50, blank=False, null= False)
    directions = models.CharField(max_length=50, blank=False, null= False)

    reception_start = models.DateField(blank=False, null= False)
    reception_end = models.DateField(blank=False, null= False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Eslatma(models.Model):
    eslatma_matni = models.CharField(max_length=300, blank=False, null= False)
    universitet = models.ForeignKey(University, on_delete=models.CASCADE, related_name='eslatma_universitet')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="eslatma_user")

    eslatma_kun = models.DateField(blank=True, null= True, verbose_name="Eslatish sanasi")
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


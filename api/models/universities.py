from django.db import models




class University(models.Model):
    university_name = models.CharField(max_length=100, blank=False, null= False)
    state = models.CharField(max_length=100, blank=False, null= False)

    level = models.CharField(max_length=50, blank=False, null= False)
    grant_name = models.CharField(max_length=100, blank=False, null= False)

    grand_amount = models.IntegerField(blank=False, null= False)
    grand_turi = models.CharField(max_length=50, blank=False, null= False)
    directions = models.CharField(max_length=50, blank=False, null= False)

    reception_start = models.DateField(blank=False, null= False)
    reception_end = models.DateField(blank=False, null= False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
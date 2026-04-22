from django.db import models
from api.models import User

# Create your models here.


PROVIDER_CHOICES = (
    ("click", "Click"),
    ("payme", "Payme"),
)

STATUS_CHOICES = (
    ("pending", "Pending"),
    ("completed", "Completed"),
    ("failed", "Failed"),
    ("cancelled", "Cancelled"),
)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.user.email} - {self.amount} - {self.provider} - {self.status}"


    class Meta:
        ordering = ['-created_at']
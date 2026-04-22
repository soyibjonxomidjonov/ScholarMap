from rest_framework import serializers
from billing.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id', 'user', 'provider', 'status', 'transaction_id', 'created_at']


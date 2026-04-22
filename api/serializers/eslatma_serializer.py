from rest_framework import serializers
from api.models import Eslatma

class EslatmaSerializerConfig(serializers.ModelSerializer):
    class Meta:
        model = Eslatma
        fields = ["id", "eslatma_matni", "universitet", "user", "eslatma_kun","ogohlantirish_sms" ,"qolgan_kun",
                  "tugash_kun", 'chat_id',
                  "updated_at", "created_at"]
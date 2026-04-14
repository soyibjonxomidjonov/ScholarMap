from rest_framework import serializers
from api.models import Eslatma

class EslatmaSerializerConfig(serializers.ModelSerializer):
    class Meta:
        model = Eslatma
        fields = ["id", "eslatma_matni", "universitet", "user", "eslatma_kun", "qolgan_kun", "tugash_kun",
                  "updated_at", "created_at"]
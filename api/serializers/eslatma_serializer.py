from rest_framework import serializers
from api.models import Eslatma

class EslatmaSerializerConfig(serializers.ModelSerializer):
    class Meta:
        model = Eslatma
        fields = '__all__'
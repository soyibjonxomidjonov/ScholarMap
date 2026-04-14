from rest_framework import serializers
from api.models import Eslatma

class EslatmaSerializerConfig(serializers.ModelSerializer):
    model = Eslatma
    fields = '__all__'
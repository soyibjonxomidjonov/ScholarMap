from rest_framework import serializers
from api.models import University

class UniversitySerializerConfig(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'

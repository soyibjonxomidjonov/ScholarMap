from rest_framework import serializers


class TranslateSerializerConfig(serializers.ModelSerializer):
    text = serializers.CharField(max_length=1500, required=False, allow_blank=True)

    file = serializers.FileField(required=False, allow_null=True)

    target_lang = serializers.CharField(max_length=10, required=True)
from rest_framework import serializers


class TranslateSerializerConfig(serializers.Serializer):
    text = serializers.CharField(max_length=1500, required=False, allow_blank=True)
    file = serializers.FileField(required=False, allow_null=True)
    target_lang = serializers.CharField(max_length=10, required=False, allow_null=True)
    response_type = serializers.CharField(max_length=10, required=False, allow_blank=True, default="text")


class ChatMessageSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=['user', 'assistant'])
    content = serializers.CharField()


class AssistantSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=5000,
        help_text="Foydalanuvchining savoli yoki xabari."
    )
    chat_history = ChatMessageSerializer(
        many=True, required=False, default=[],
        help_text="Oldingi suhbat tarixi (frontend tomonidan saqlanadi)."
    )
    with_universities = serializers.BooleanField(
        required=False, default=False,
        help_text="True bo'lsa, AI universitetlar ma'lumotini ham ko'radi."
    )


class UniversityMatchSerializer(serializers.Serializer):
    directions = serializers.CharField(
        max_length=200, required=False, allow_blank=True,
        help_text="O'qishni xohlaydigan yo'nalish (masalan: IT, Medicine, Business)"
    )
    level = serializers.CharField(
        max_length=50, required=False, allow_blank=True,
        help_text="Ta'lim darajasi: Bachelor, Master, PhD"
    )
    state = serializers.CharField(
        max_length=100, required=False, allow_blank=True,
        help_text="Qaysi mamlakatda o'qishni xohlaydi?"
    )
    grand_turi = serializers.CharField(
        max_length=100, required=False, allow_blank=True,
        help_text="Grant turi (masalan: to'liq grant, qisman grant)"
    )
    additional_info = serializers.CharField(
        max_length=1000, required=False, allow_blank=True,
        help_text="Qo'shimcha ma'lumot (masalan: til darajasi, ball va hokazo)"
    )
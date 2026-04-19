from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializerConfig(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "id", "password" , "first_name", "phone_number", "last_name",
                  "sharif","image", "lang", "created_at"]
        extra_kwargs = {'password': {'write_only': True}, 'is_active': {'read_only': True}}


    def create(self, validated_data):
        # Username majburiy bo'lgani uchun unga emailni berib yuboramiz
        validated_data['username'] = validated_data.get('email')
        user = User.objects.create_user(**validated_data)
        user.is_active = True  # ✅ Shu yerda aniq belgilang
        user.save(update_fields=['is_active'])  # ✅ Bu qator bo'lmasa DB ga saqlanmaydi!
        return user







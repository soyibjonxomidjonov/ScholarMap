from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializerConfig(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "phone_number", "last_name", "sharif","image", "lang", "created_at"]

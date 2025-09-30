from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "city",
            "avatar",
            "is_active",
            "is_staff",
        )
        read_only_fields = ("id", "is_staff", "is_active")
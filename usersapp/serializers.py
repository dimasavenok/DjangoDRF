from rest_framework import serializers
from .models import User, Payment


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

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
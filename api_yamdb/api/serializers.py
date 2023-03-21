from rest_framework import serializers

from reviews.models import User


class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "email",
            "username",
        )
        model = User

    def create(self, validated_data):
        user = User.objects.update_or_create(**validated_data)
        return user

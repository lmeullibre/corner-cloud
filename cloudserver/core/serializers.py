from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import Game
import uuid

User = get_user_model()


class ConnectionParametersSerializer(serializers.Serializer):
    hostname = serializers.CharField(max_length=100)
    port = serializers.IntegerField()
    protocol = serializers.CharField(max_length=10)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data.get("username"), password=data.get("password")
        )
        if user is None:
            raise serializers.ValidationError("Invalid username/password.")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive.")
        return data


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", "name", "coming_soon"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "name_tag")
        extra_kwargs = {
            "name_tag": {"required": False},  # Make name_tag not required
        }

    def create(self, validated_data):
        # Assuming username is unique and can serve as the base for name_tag
        base_name_tag = validated_data["username"]
        unique_name_tag = base_name_tag
        num = 1

        # Generate a unique name_tag if necessary
        while User.objects.filter(name_tag=unique_name_tag).exists():
            unique_name_tag = f"{base_name_tag}_{num}"
            num += 1

        user = User.objects.create(
            username=validated_data["username"],
            name_tag=unique_name_tag,  # Use the generated unique name_tag
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

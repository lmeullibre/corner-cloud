from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Game

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
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if user is None:
            raise serializers.ValidationError("Invalid username/password.")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive.")
        return data
    
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id','name', 'coming_soon']
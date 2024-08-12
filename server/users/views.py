from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from games.models import Game
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer, CustomTokenObtainPairSerializer
from django.http import JsonResponse
from .utils import encrypt_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import docker

class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_token(request, slug):
    # Retrieve the game by slug
    game = get_object_or_404(Game, slug=slug)
    
    # Generate a unique container name using the game slug and the username
    container_name = f"{game.slug}_{request.user.username}"
    
    client = docker.from_env()

    try:
        # Get the container object by name
        container = client.containers.get(container_name)

        # Access the network settings to get the IP address
        network_info = container.attrs['NetworkSettings']['Networks']
        ip_address = None
        for network_name, settings in network_info.items():
            ip_address = settings.get('IPAddress')
            if ip_address:
                break  # Stop once we find a valid IP address

        if not ip_address:
            return JsonResponse({"error": "Could not retrieve IP address for the container."}, status=500)

        # Generate the token object with the correct IP address
        token_object = {
            "connection": {
                "type": "ssh",
                "settings": {
                    "hostname": ip_address,
                    "port": "22",
                    "username": "root",
                    "password": "password",
                },
            }
        }

        token = encrypt_token(token_object)
        return JsonResponse({"token": token})

    except docker.errors.NotFound:
        return JsonResponse({"error": "Container not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)
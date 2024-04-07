from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import requests
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import ConnectionParametersSerializer
import jwt
from django.http import JsonResponse
import base64, json
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hmac
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer
from .models import Game
from .serializers import GameSerializer
from rest_framework.permissions import IsAuthenticated  # Ensure users are authenticated
from .models import Game, GameUser
from .services import get_or_create_game_user
from django.conf import settings
from .serializers import UserRegistrationSerializer


class GuacamoleAdminAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Admin username"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Admin password"
                ),
            },
        ),
        responses={200: "Success"},
    )
    def post(self, request, *args, **kwargs):
        admin_username = request.data.get("username")
        admin_password = request.data.get("password")

        if not admin_username or not admin_password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authenticate and get an authToken
        auth_token = self.get_auth_token(admin_username, admin_password)
        if not auth_token:
            return Response(
                {"error": "Authentication failed."}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Retrieve all connections
        connections = self.get_guacamole_connections(auth_token)
        if connections is None:
            return Response(
                {"error": "Failed to retrieve connections."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(connections)

    def get_auth_token(self, username, password):
        """Authenticate and get an authToken."""
        response = requests.post(
            f"{settings.GUACAMOLE_URL}api/tokens",
            data={"username": username, "password": password},
        )
        if response.status_code == 200:
            return response.json().get("authToken")
        else:
            return None

    def get_guacamole_connections(self, auth_token):
        """Get the list of all connections using the authToken."""
        connections_url = f"{settings.GUACAMOLE_URL}api/session/data/mysql/connections?token={auth_token}"
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(connections_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print("-------")
            print(response.text)
            return Response(
                {
                    "error": "Failed to retrieve connections.",
                    "status_code": response.status_code,
                    "details": response.text,
                },
                status=response.status_code,
            )


# Create your views here.
def index(request):
    return HttpResponse("Hello, cloud gaming world!")


@method_decorator(csrf_exempt, name="dispatch")
class GenerateGuacamoleTokenViewExpert(APIView):
    permission_classes = [IsAuthenticated]  # Apply the authentication requirement

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "game_id",
                openapi.IN_QUERY,
                description="ID of the game",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        game_id = request.GET.get(
            "game_id"
        )  # Fetching the game ID from query parameters

        try:
            # Fetch the GameUser instance for the given game ID and logged-in user
            game_user = get_or_create_game_user(request.user, game_id)

            # Dynamically fill in the connection details from the GameUser instance
            game_details_mapping = {
                "connection": {
                    "type": "ssh",
                    "settings": {
                        "hostname": game_user.vm_ip,
                        "port": game_user.vm_port,
                        "username": game_user.vm_username,
                        "password": game_user.vm_password,
                    },
                }
            }

            SECRET_KEY = b"MySuperSecretKeyForParamsToken12"

            def encrypt_token(value):
                iv = os.urandom(16)
                cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
                padded_data = pad(json.dumps(value).encode(), AES.block_size)
                encrypted_data = cipher.encrypt(padded_data)
                data = {
                    "iv": base64.b64encode(iv).decode("utf-8"),
                    "value": base64.b64encode(encrypted_data).decode("utf-8"),
                }
                json_data = json.dumps(data)
                return base64.b64encode(json_data.encode()).decode("utf-8")

            encrypted_token = encrypt_token(game_details_mapping)

            return JsonResponse({"guacamoleToken": encrypted_token})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User's username"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User's password"
                ),
            },
            required=["username", "password"],
            description="Credentials for user login",
        ),
        responses={
            200: openapi.Response("Login Successful"),
            400: "Invalid Credentials",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )
        if user:
            login(request, user)  # This attaches the user to the current session
            return Response({"message": "User logged in successfully."})
        else:
            return Response({"message": "Invalid credentials."}, status=400)


class GameList(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Game.objects.all()
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)


class UserRegistrationView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User's username"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User's password"
                ),
            },
            required=["username", "password"],
            description="Registration credentials",
        ),
        responses={
            201: openapi.Response(
                "Registration Successful", UserRegistrationSerializer
            ),
            400: "Invalid input",
        },
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"user": serializer.data, "message": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

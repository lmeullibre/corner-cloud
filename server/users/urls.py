from django.urls import path
from .views import UserCreate, CustomTokenObtainPairView, generate_token
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserCreate, CustomTokenObtainPairView, get_current_user
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', UserCreate.as_view(), name='api_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', get_current_user, name='get_current_user'),
    path('generate-guacamole-token/<slug:slug>/', generate_token, name='generate_token'),
    path('django-login/', auth_views.LoginView.as_view(), name='login'),  # Add this for session-based login
    path('django-logout/', auth_views.LogoutView.as_view(), name='logout'),
] 
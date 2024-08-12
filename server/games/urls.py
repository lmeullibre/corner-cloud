from django.urls import path
from .views import GameListView, GameDetailBySlugView, get_container_network_info
from .views import launch_game, shutdown_game, check_container_status

urlpatterns = [
    path('', GameListView.as_view(), name='game-list'),
    path('<slug:slug>/', GameDetailBySlugView.as_view(), name='game-detail-by-slug'),
    path('<slug:slug>/launch/', launch_game, name='launch_game'),
    path('<slug:slug>/shutdown/', shutdown_game, name='shutdown_game'),
    path('<slug:slug>/check-status/', check_container_status, name='check_container_status'),
    path('container-network/<str:container_name>/', get_container_network_info, name='get_container_network_info'),
]
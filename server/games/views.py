from rest_framework import generics
from .models import Game
from .serializers import GameSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import subprocess
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import docker

class GameListView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameDetailView(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

def user_has_permission_for_container(request, container_name):
    """
    Checks if the container name corresponds to the current user's container.
    Assumes the container_name format is "<game_slug>_<username>".
    """
    expected_container_name = f"{container_name.split('_')[0]}_{request.user.username}"
    return container_name == expected_container_name

def disconnect_and_remove_network(network_name):
    """
    Disconnect all containers from the network and then remove the network.
    """
    client = docker.from_env()

    try:
        # Retrieve the network
        network = client.networks.get(network_name)

        # Disconnect all containers from the network
        for container in network.containers:
            try:
                network.disconnect(container, force=True)
            except docker.errors.APIError as e:
                return {'error': f'Failed to disconnect container {container.name} from the network: {str(e)}'}
        
        # After disconnecting all containers, proceed to remove the network
        network.remove()
        return {'success': f'Network {network_name} has been removed successfully.'}

    except docker.errors.NotFound:
        return {'error': f'Network {network_name} does not exist.'}
    except docker.errors.APIError as e:
        return {'error': str(e)}



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def launch_game(request, slug):
    # Retrieve the game by slug
    game = get_object_or_404(Game, slug=slug)
    
    # Generate a unique container name and network name using the game name and username
    container_name = f"{game.slug}_{request.user.username}"
    network_name = f"{container_name}_network"
    
    client = docker.from_env()

    # Check if the container already exists
    try:
        client.containers.get(container_name)
        return Response(
            {'error': f'Container {container_name} already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except docker.errors.NotFound:
        pass  # Container does not exist, proceed to create it
    except docker.errors.APIError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Attempt to create the network
    try:
        client.networks.create(network_name)
    except docker.errors.APIError as e:
        return Response({'error': f'Failed to create network: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    try:
        # Determine whether to include the entry_point command
        container_args = {
            "image": game.docker_image,
            "name": container_name,
            "detach": True,
            "network": network_name,
            "ports": {f'{game.internal_port}/tcp': game.port},  # Dynamic internal port based on the service type,
        }

        if game.entry_point:
            container_args["command"] = game.entry_point

        # Run the game container with or without a specific entry point
        container = client.containers.run(**container_args)

        # Connect essential services to the new network
        essential_services = ['guacamole', 'guacd', 'nginx', 'guac_mysql', 'lite-server']
        for service in essential_services:
            try:
                service_container = client.containers.get(service)
                network = client.networks.get(network_name)
                network.connect(service_container)
            except docker.errors.APIError as e:
                return Response({'error': f'Failed to connect {service} to the network: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except docker.errors.APIError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Generate the access URL based on the service type
    if game.internal_port == 22:
        play_url = f'ssh root@{request.get_host()} -p {game.port}'
    elif game.internal_port == 5900:
        play_url = f'vnc://{request.get_host()}:{game.port}'
    else:
        play_url = f'{request.get_host()}:{game.port}'

    return Response({'container_name': container_name, 'play_url': play_url}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def shutdown_game(request, slug):
    try:
        game = Game.objects.get(slug=slug)
    except Game.DoesNotExist:
        raise NotFound(detail="Game not found", code=status.HTTP_404_NOT_FOUND)
    
    # Generate the container name based on the game slug and username
    container_name = f"{game.slug}_{request.user.username}"

    # Check if the container belongs to the current user
    if not user_has_permission_for_container(request, container_name):
        return Response(
            {'error': 'You do not have permission to shut down this container.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    client = docker.from_env()

    try:
        # Retrieve the container
        container = client.containers.get(container_name)
        
        # Stop the container
        container.stop()
        
        # Remove the container
        container.remove()

        # Retrieve the network
        network_name = f"{container_name}_network"
        network = client.networks.get(network_name)

        # Disconnect essential services from the network
        essential_services = ['guacamole', 'guacd', 'nginx', 'guac_mysql', 'lite-server']
        for service in essential_services:
            try:
                network.disconnect(service)
            except docker.errors.APIError as e:
                # Log error or handle exceptions if needed
                pass
        
        # Remove the network
        network.remove()

    except docker.errors.NotFound:
        return Response(
            {'error': f'Container {container_name} or its network does not exist.'},
            status=status.HTTP_404_NOT_FOUND
        )
    except docker.errors.APIError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': f'Container {container_name} and its network have been stopped and removed.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_container_status(request, slug):
    # Retrieve the game by slug
    game = get_object_or_404(Game, slug=slug)

    # Generate the container name based on the game slug and username
    container_name = f"{game.slug}_{request.user.username}"

    # Check if the container belongs to the current user
    if not user_has_permission_for_container(request, container_name):
        return Response(
            {'error': 'You do not have permission to check the status of this container.'},
            status=status.HTTP_403_FORBIDDEN
        )

    client = docker.from_env()

    try:
        # Retrieve the container
        container = client.containers.get(container_name)
        
        # Get the container status
        container_status = container.status
        
        # Map the Docker status to your API response
        if container_status == "running":
            return Response({'status': 'ready'}, status=200)
        elif container_status in ["created", "restarting"]:
            return Response({'status': 'starting'}, status=202)
        elif container_status == "exited":
            return Response({'status': 'stopped'}, status=200)
        elif container_status == "paused":
            return Response({'status': 'paused'}, status=200)
        else:
            return Response({'status': 'unknown', 'details': container_status}, status=200)

    except docker.errors.NotFound:
        return Response({'status': 'error', 'message': 'Container does not exist'}, status=404)
    except docker.errors.APIError as e:
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_container_network_info(request, container_name):
    client = docker.from_env()

    try:
        # Get the container object by name
        container = client.containers.get(container_name)

        # Access network settings
        network_info = container.attrs['NetworkSettings']['Networks']
        network_data = {}
        
        # Extract useful information from network settings
        for network_name, settings in network_info.items():
            network_data[network_name] = {
                'IPAddress': settings.get('IPAddress'),
                'MacAddress': settings.get('MacAddress'),
                'Gateway': settings.get('Gateway'),
                'Subnet': settings.get('Subnet'),
            }

        return JsonResponse({
            'container_name': container_name,
            'networks': network_data
        })

    except docker.errors.NotFound:
        return Response({'error': 'Container not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_game_network(request, slug):
    try:
        game = Game.objects.get(slug=slug)
    except Game.DoesNotExist:
        raise NotFound(detail="Game not found", code=status.HTTP_404_NOT_FOUND)
    
    # Generate the container and network name based on the game slug and username
    container_name = f"{game.slug}_{request.user.username}"
    network_name = f"{container_name}_network"

    # Check if the network belongs to the current user's container
    if not user_has_permission_for_container(request, container_name):
        return Response(
            {'error': 'You do not have permission to remove this network.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Use the helper function to disconnect and remove the network
    network_response = disconnect_and_remove_network(network_name)
    if 'error' in network_response:
        return Response(network_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': network_response['success']}, status=status.HTTP_200_OK)


    
class GameDetailBySlugView(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'slug'
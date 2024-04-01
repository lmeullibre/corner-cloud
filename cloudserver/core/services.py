# services.py
from .models import Game, GameUser
from django.conf import settings

def get_or_create_game_user(user, game_id):
    game_user = GameUser.objects.filter(game__id=game_id, user=user).first()

    if not game_user:
        # If GameUser does not exist, create one
        vm_password = settings.VM_PASSWORD
        vm_ip = '127.0.0.1'
        vm_protocol = 'ssh'
        vm_port = 22
        vm_username = f"{user.name_tag}_{game_id}"

        # Fetch the game by id
        game = Game.objects.get(id=game_id)

        # Create the GameUser instance
        game_user = GameUser.objects.create(
            user=user,
            game=game,
            vm_username=vm_username,
            vm_password=vm_password,
            vm_ip=vm_ip,
            vm_protocol=vm_protocol,
            vm_port=vm_port
        )

    return game_user

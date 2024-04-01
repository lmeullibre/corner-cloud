from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    coming_soon = models.BooleanField(default=False)
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, through='GameUser', related_name='games')

    def __str__(self):
        return self.name

class GameUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    vm_username = models.CharField(max_length=100)
    vm_password = models.CharField(max_length=100)
    vm_ip = models.GenericIPAddressField()
    vm_protocol = models.CharField(max_length=10)
    vm_port = models.IntegerField()

    class Meta:
        unique_together = ('user', 'game')  # Ensures the combination of user and game is unique

    def __str__(self):
        return f"{self.user.username} plays {self.game.name}"
        
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_tag = models.CharField(max_length=100, unique=True)
    
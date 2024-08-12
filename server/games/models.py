from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    docker_image = models.CharField(max_length=255)
    entry_point = models.CharField(max_length=255)
    port = models.IntegerField()

    def __str__(self):
        return self.name
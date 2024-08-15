from django.db import models

class Game(models.Model):
    # Existing fields
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    docker_image = models.CharField(max_length=255)
    entry_point = models.CharField(max_length=255, blank=True, null=True)
    port = models.IntegerField()  # External port

    # New field for the internal port
    internal_port = models.IntegerField(default=22)  # Defaulting to 22 for SSH

    # Other fields...

    def __str__(self):
        return self.name
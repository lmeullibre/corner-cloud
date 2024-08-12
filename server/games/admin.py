from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'docker_image', 'entry_point', 'port')
    search_fields = ('name', 'slug', 'docker_image')

# Alternatively, you can register the model without a decorator:
# admin.site.register(Game, GameAdmin)
from django.contrib import admin
from .models import Player, Match, Team

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)

# Register your models here.

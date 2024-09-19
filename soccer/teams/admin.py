from django.contrib import admin

from .models import Player, Match, Score, Team

admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Score)
admin.site.register(Team)
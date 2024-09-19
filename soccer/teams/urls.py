from django.urls import path

from . import views

app_name = "teams"
urlpatterns = [
    path("", views.home, name="home"),
    path("player/", views.player, name="player"),
    path("players/", views.players, name="players"),
    path("player/selection/", views.team_split, name="split_teams"),
    path("match/", views.get_matches, name="matches"),
]
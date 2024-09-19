from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Player, Team, Match, Score
from .utils.split import Assigner
from .utils.split import Player as PlayerClass

import json

def home(request):
    template = loader.get_template("teams/home.html")
    return HttpResponse(template.render({}, request))

def player(request):
    if request.method == "GET":
        template = loader.get_template("teams/createuser.html")
        return HttpResponse(template.render({}, request))

    elif request.method == "POST":
        player = Player(name=request.POST["name"], skill_rating=request.POST["skill"],
                        preferred_position=request.POST["ppos"], secondary_position=request.POST["spos"],
                        gender=request.POST["gender"])
        
        player.save()

        template = loader.get_template("teams/pcreated.html")
        return HttpResponse(template.render({"user": request.POST["name"]}, request))
    
def players(request):
    print(request.GET["gender"])
    players_ = Player.objects.filter(gender=request.GET["gender"])

    template = loader.get_template("teams/playerlist.html")

    return HttpResponse(template.render({"players": players_}, request))

def team_split(request):
    if request.method == 'GET':
        players_ = Player.objects.filter(gender=request.GET["gender"])

        template = loader.get_template("teams/selectusers.html")

        return HttpResponse(template.render({"players": players_}, request))
    elif request.method == 'POST':
        players_list = []
        
        for player_id in request.POST.getlist('selected_players'):
            player_ = Player.objects.get(pk=int(player_id))
            players_list.append(PlayerClass(int(player_id), player_.name, player_.skill_rating, player_.preferred_position.lower(), player_.secondary_position.lower()))
        
        team1, team2 = Assigner.balance_teams(players_list)

        print(team1, team2)

        team1_ = Team()
        team2_ = Team()

        team1_.save()
        team2_.save()

        for ply in team1:
            print("T1 Player: ", ply)
            team1_.players.add(Player.objects.get(pk=ply.id))

        for ply in team2:
            print("T2 Player: ", ply)
            team2_.players.add(Player.objects.get(pk=ply.id))

        team1_.save()
        team2_.save()

        template = loader.get_template("teams/split.html")

        score = Score(team_one_score=0, team_two_score=0)
        score.save()
        match = Match(match_date=timezone.now(), score=score)
        match.save()
        match.teams.add(team1_)
        match.teams.add(team2_)

        return HttpResponse(template.render({"team_one": team1_, "team_two": team2_}, request))
    

def get_matches(request):
    matches = Match.objects.all().order_by('match_date')
    selected_match = None

    match_id = request.GET.get('match_id')
    if match_id:
        selected_match = get_object_or_404(Match, id=match_id)

    template = loader.get_template("teams/matches.html")

    context = {
        'matches': matches,
        'selected_match': selected_match,
    }
    return HttpResponse(template.render(context, request))
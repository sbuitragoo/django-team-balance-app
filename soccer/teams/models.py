from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=50)
    skill_rating = models.FloatField(default=3.0)
    preferred_position = models.CharField(max_length=30)
    secondary_position = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, default='M')

    def __str__(self) -> str:
        return self.name

class Team(models.Model):
    players = models.ManyToManyField(Player)

class Score(models.Model):
    team_one_score = models.IntegerField()
    team_two_score = models.IntegerField()

class Match(models.Model):
    teams = models.ManyToManyField(Team)
    match_date = models.DateTimeField()
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
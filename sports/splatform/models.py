from django.db import models


class Player(models.Model):
    player_name = models.CharField(max_length=100)
    player_team = models.CharField(max_length=100)
    goal = models.IntegerField(default=0)
    assist = models.IntegerField(default=0)
    y_card = models.IntegerField(default=0)
    r_card = models.IntegerField(default=0)

    def __str__(self):
        return self.player_name


class Match(models.Model):
    match_no = models.IntegerField(default=0)
    h_team = models.CharField(max_length=100)
    a_team = models.CharField(max_length=100)
    h_goal = models.IntegerField(default=0)
    a_goal = models.IntegerField(default=0)

    def __str__(self):
        return self.match_no


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    group = models.CharField(max_length=100)

    def __str__(self):
        return self.team_name


# 用户名密码的django好像有专门的一个模块，先研究一下其他的数据
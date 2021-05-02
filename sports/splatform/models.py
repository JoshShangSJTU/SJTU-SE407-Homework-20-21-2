from django.db import models


class Player(models.Model):
    # 运动员模型
    player_name = models.CharField(max_length=30) # 运动员名字
    # player_team = models.CharField(max_length=50) # 运动员所在队伍
    goal = models.IntegerField(default=0) # 总进球数
    assist = models.IntegerField(default=0) # 总助攻数
    y_card = models.IntegerField(default=0) # 黄牌数
    r_card = models.IntegerField(default=0) # 红牌数

    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE) # 定义外键，Team和Player是1:n

    def __str__(self):
        return self.player_name


class Match(models.Model):
    match_id = models.IntegerField(default=0) # 比赛序号
    h_team_id = models.ForeignKey(Team, related_name='h_team', on_delete=models.CASCADE) # 主队
    a_team_id = models.ForeignKey(Team, related_name='a_team', on_delete=models.CASCADE) # 客队

    h_score = models.IntegerField(default=0) # 主队进球数
    a_score = models.IntegerField(default=0) # 客队进球数
    
    match_time = models.DateTimeField() # 比赛时间
    match_loc = models.CharField(max_length=20) # 比赛地点

    def __str__(self):
        return self.match_no


class Team(models.Model):
    team_name = models.CharField(max_length=50) # 队伍名
    coach = models.CharField(max_length=20) # 主教练
    group = models.CharField(max_length=100) # 小组名

    def __str__(self):
        return self.team_name


# 用户名密码的django好像有专门的一个模块，先研究一下其他的数据
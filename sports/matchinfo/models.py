from django.db import models

from splatform.models import Match, Team, Player

# Create your models here.
class Package(models.Model):
    
    match_no = models.IntegerField('比赛编号', default=0)
    match_loc = models.CharField('比赛地点', max_length=50,default='')
    match_time = models.CharField('比赛时间',max_length=50,default='')

    h_team_name = models.CharField('主队伍名', max_length=50,default='')
    h_match_score = models.IntegerField('主队进球', default=0)
    h_player_set = models.CharField('主队员表', max_length=100,default='')

    a_team_name = models.CharField('客队伍名', max_length=50,default='')
    a_match_score = models.IntegerField('客队进球', default=0)
    a_player_set = models.CharField('客队员表', max_length=100,default='')

    class Meta:
        verbose_name_plural = '详情表'

    def __str__(self):
        return str(self.match_no)

    def init(): #初始化表
        for match in Match.objects.all():

            teamh = Team.objects.get(pk=match.h_team_name_id)
            teama = Team.objects.get(pk=match.a_team_name_id)  

            playerh = Player.objects.filter(team_id=match.h_team_name_id)
            playerhset = []
            for player in playerh:
                playerhset.append(player.player_name) 
                                
            playera = Player.objects.filter(team_id=match.a_team_name_id)
            playeraset = []
            for player in playera:
                playeraset.append(player.player_name)
            
            timeinfo = str(match.match_time)    #调整时间格式
            date = timeinfo[0:10]    
            hour = (int(timeinfo[11:13])+8)%24
            if hour < 10:
                hour = '0'+str(hour)
            else:
                hour = str(hour)
            minute = timeinfo[14:16]

            timepack=(date,hour,minute)

            Flag_not_in = True

            for i in Package.objects.filter(match_no=match.match_no):
                Flag_not_in =False
            

            if Flag_not_in:   
                Package.objects.create(
                    match_no = match.match_no,
                    match_loc = match.match_loc,
                    match_time = str(timepack),

                    h_team_name = teamh.team_name,
                    h_match_score = match.h_score,
                    h_player_set = str(playerhset),

                    a_team_name = teama.team_name,
                    a_match_score = match.a_score,
                    a_player_set = str(playeraset),
                )

    def delete(key):
        Package.objects.filter(match_no=key).delete()
    
    def clear():
        Package.objects.all().delete()
from django.db import models

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

    def delete(key):
        Package.objects.filter(match_no=key).delete()
    
    def clear():
        Package.objects.all().delete()
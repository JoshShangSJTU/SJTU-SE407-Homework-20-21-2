from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

from splatform import models
# Create your views here.

'''
查询语法：
.all()  选择全部对象
.filter()   筛选符合括号内筛选条件的对象
    如：    models.Book.objects.filter(pk=5)
    pk为primary key，代表数据库中的id

.exclude() 筛选不符合括号内筛选条件的对象
.get()      筛选对象，且只能返回一个对象，否则报错
.order_by() 方法用于对查询结果进行排序
    a、参数的字段名要加引号。
    b、降序为在字段前面加个负号 -。
        如：    models.Book.objects.order_by(-"price")

count() 方法用于查询数据的数量，返回的数据是整数

'''
'''副本
def Homedata(request):
    
    #DjangoJSONEncoder("UTF-8")

    match_package = []
    player_package = []
    team_package = []

    for match in models.Match.objects.all():
        matchinfo={'id':match.pk,'match_no':match.match_no,'h_score':match.h_score,'a_score':match.a_score,'match_loc':match.match_loc,'a_team_name_id':match.a_team_name_id,'h_team_name_id':match.h_team_name_id,'match_time':match.match_time}
        match_package.append(matchinfo)

    for player in models.Player.objects.all():       
        playerinfo={'id':player.pk,'name':player.player_name,'goal':player.goal,'assist':player.assist,'r_card':player.r_card,'team_id':player.team_id,'y_card':player.y_card}
        player_package.append(playerinfo)

    for team in models.Team.objects.all():       
        teaminfo={'id':team.pk,'team_name':team.team_name,'coach':team.coach,'group':team.group,'point':team.point}
        team_package.append(teaminfo)

        package={'Match_package':match_package,'Player_package':player_package,'Team_package':team_package}
    return JsonResponse(package,safe=False,json_dumps_params={'ensure_ascii':False})
'''

def Homedata(request):
    
    package=[]
    
    for match in models.Match.objects.all():

        teamh = models.Team.objects.get(pk=match.h_team_name_id)
        teama = models.Team.objects.get(pk=match.a_team_name_id)            
        info={'比赛编号':match.match_no,'主队队名':teamh.team_name,'客队队名':teama.team_name,'比赛地点':match.match_loc,'比赛时间':match.match_time}
        package.append(info)

    return JsonResponse(package,safe=False,json_dumps_params={'ensure_ascii':False})

def Detaildata(request):
   
    package=[]

    for match in models.Match.objects.all():

        teamh = models.Team.objects.get(pk=match.h_team_name_id)
        teama = models.Team.objects.get(pk=match.a_team_name_id)  

        playerh = models.Player.objects.filter(team_id=match.h_team_name_id)
        playerhset = []
        for player in playerh:
            playerhset.append(player.player_name) 
                       
        playera = models.Player.objects.filter(team_id=match.a_team_name_id)
        playeraset = []
        for player in playera:
            playeraset.append(player.player_name)

        H_info = {'主队队名':teamh.team_name,'主队得分':match.h_score,'队员表':playerhset}
        print (H_info)
        A_info = {'客队队名':teama.team_name,'客队得分':match.a_score,'队员表':playeraset}
        print (A_info)
        baseinfo= {'比赛编号':match.match_no,'比赛地点':match.match_loc,'比赛时间':match.match_time}
        info = {'比赛信息':baseinfo,'主队信息':H_info,'客队信息':A_info}
        package.append(info)
    return JsonResponse(package,safe=False,json_dumps_params={'ensure_ascii':False})
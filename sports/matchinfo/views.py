from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.generic import ListView

from splatform import models
from .models import Package
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
def Homedata(request,page):  #向赛事信息列表发送数据的视图
    
    Package.refresh()

    page=int(page)
    package=[]
    count = 0
    for match in models.Match.objects.all():
        count += 1

        teamh = models.Team.objects.get(pk=match.h_team_name_id)    #获取比赛的两支队伍信息
        teama = models.Team.objects.get(pk=match.a_team_name_id)  

        timeinfo = str(match.match_time)    #调整时间格式
        date = timeinfo[0:10]    
        hour = str((int(timeinfo[11:13])+8)%24)
        minute = timeinfo[14:16]

        info={'比赛编号':match.match_no,'主队队名':teamh.team_name,'客队队名':teama.team_name,'比赛地点':match.match_loc,'比赛时间':(date,hour,minute)}      

        package.append(info)

    split_package = package[6*(page-1):6*page]

    dict1={'COUNT':count}
    dict2={'本页比赛':split_package}
    PACKAGE = [dict1,dict2]

    return JsonResponse(PACKAGE,safe=False,json_dumps_params={'ensure_ascii':False})



def Detaildata(request,para,sign):    #向详情页发送数据的视图

    checklist = []
    for match in models.Match.objects.all():
        checklist.append(match.match_no)

    print(para)
    print(sign)

    para = int(sign+para)
    
    if para not in checklist:        
        return JsonResponse("没有该比赛编号！",safe=False,json_dumps_params={'ensure_ascii':False})
        
    if para not in checklist:        
        return JsonResponse("没有该比赛编号！",safe=False,json_dumps_params={'ensure_ascii':False})
        
    h_player_set=[]
    a_player_set=[]

    for match in models.Match.objects.all():
        teamh = models.Team.objects.get(pk=match.h_team_name_id)
        teama = models.Team.objects.get(pk=match.a_team_name_id)  

        playerh = models.Player.objects.filter(team_id=match.h_team_name_id)
        playerhset = []
        for player in playerh:
            playerhset.append(player.player_name) 
        h_player_set=playerhset
                            
        playera = models.Player.objects.filter(team_id=match.a_team_name_id)
        playeraset = []
        for player in playera:
            playeraset.append(player.player_name)
        a_player_set=playeraset

    info = Package.objects.all().get(match_no=para)
    H_info = {'主队队名':info.h_team_name,'主队得分':info.h_match_score,'队员表':h_player_set}
    A_info = {'客队队名':info.a_team_name,'客队得分':info.a_match_score,'队员表':a_player_set}
    baseinfo= {'比赛编号':info.match_no,'比赛地点':info.match_loc,'比赛时间':info.match_loc}
    info = {'比赛信息':baseinfo,'主队信息':H_info,'客队信息':A_info}

    return JsonResponse(info,safe=False,json_dumps_params={'ensure_ascii':False})



'''
def Detaildata(request):    #向详情页发送数据的视图
   
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

        timeinfo = str(match.match_time)    #调整时间格式
        date = timeinfo[0:10]    
        hour = (int(timeinfo[11:13])+8)%24
        if hour < 10:
            hour = '0'+str(hour)
        else:
            hour = str(hour)
        minute = timeinfo[14:16]

        H_info = {'主队队名':teamh.team_name,'主队得分':match.h_score,'队员表':playerhset}
        A_info = {'客队队名':teama.team_name,'客队得分':match.a_score,'队员表':playeraset}
        baseinfo= {'比赛编号':match.match_no,'比赛地点':match.match_loc,'比赛时间':(date,hour,minute)}
        info = {'比赛信息':baseinfo,'主队信息':H_info,'客队信息':A_info}

        package.append(info)
    return JsonResponse(package,safe=False,json_dumps_params={'ensure_ascii':False})
'''
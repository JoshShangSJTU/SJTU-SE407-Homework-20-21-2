from django.shortcuts import render
from django.http.response import HttpResponse

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
def Homedata(request):
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
    return {'Match_package':match_package,'Player_package':player_package,'Team_package':team_package}

def Query(request):
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
    
    print (match_package)
    print (player_package)
    print (team_package)

    # return HttpResponse("<p>查找成功！</p>"+str(package))
    return render(request, 'match_detail.html', {'Match_package':match_package,'Player_package':player_package,'Team_package':team_package})

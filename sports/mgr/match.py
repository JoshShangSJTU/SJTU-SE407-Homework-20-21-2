from django.http import JsonResponse
from splatform.models import Match
import json


def dispatcher(request):
    # 根据session判断用户是否是登录的管理员用户
    if 'usertype' not in request.session:
        return JsonResponse(
            {
                'ret': 302,
                'msg': '未登录',
                'redirect': '/mgr/signin.html'
            },
            status=302)

    if request.session['usertype'] != 'mgr':
        return JsonResponse(
            {
                'ret': 302,
                'msg': '用户非mgr类型',
                'redirect': '/mgr/signin.html'
            },
            status=302)
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_match':
        return listmatch(request)
    elif action == 'add_match':
        return addmatch(request)
    elif action == 'modify_match':
        return modifymatch(request)
    elif action == 'del_match':
        return deletematch(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def listmatch(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Match.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})


def addmatch(request):

    info = request.params['data']

    # 从请求消息中 获取要添加比赛的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = Match.objects.create(
        match_no=info['match_no'],
        h_team_name=info['h_team_name'],
        a_team_name=info['a_team_name'],
        h_score=info['h_score'],
        a_score=info['a_score'],
        match_time=info['match_time'],
        match_loc=info['match_loc']
    )

    return JsonResponse({'ret': 0, 'id': record.id})


def modifymatch(request):

    # 从请求消息中 获取修改比赛的信息
    # 找到该比赛，并且进行修改操作

    matchid = request.params['id']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的比赛记录
        match = Match.objects.get(id=matchid)
    except match.DoesNotExist:
        return {'ret': 1, 'msg': f'id 为`{matchid}`的比赛不存在'}

    if 'match_no' in newdata:
        match.match_no = newdata['match_no']
    if 'h_team_name' in newdata:
        match.h_team_name = newdata['h_team_name']
    if 'a_team_name' in newdata:
        match.a_team_name = newdata['a_team_name']
    if 'h_score' in newdata:
        match.h_score = newdata['h_score']
    if 'a_score' in newdata:
        match.a_score = newdata['a_score']
    if 'match_time' in newdata:
        match.match_time = newdata['match_time']
    if 'match_loc' in newdata:
        match.match_loc = newdata['match_loc']

    # 注意，一定要执行save才能将修改信息保存到数据库
    match.save()

    return JsonResponse({'ret': 0})


def deletematch(request):

    matchid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的比赛记录
        match = Match.objects.get(id=matchid)
    except match.DoesNotExist:
        return {
                'ret': 1,
                'msg': f'id 为`{matchid}`的比赛不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    match.delete()

    return JsonResponse({'ret': 0})


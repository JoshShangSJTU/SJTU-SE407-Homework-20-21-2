from django.http import JsonResponse
from splatform.models import Team
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
    if action == 'list_team':
        return listteam(request)
    elif action == 'add_team':
        return addteam(request)
    elif action == 'modify_team':
        return modifyteam(request)
    elif action == 'del_team':
        return deleteteam(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def listteam(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Team.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})


def addteam(request):

    info = request.params['data']

    # 从请求消息中 获取要添加队伍的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = Team.objects.create(
        team_name=info['team_name'],
        coach=info['coach'],
        group=info['group'],
        point=info['point'],
    )

    return JsonResponse({'ret': 0, 'id': record.id})


def modifyteam(request):

    # 从请求消息中 获取修改队伍的信息
    # 找到该队伍，并且进行修改操作

    teamid = request.params['id']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的队伍记录
        team = Team.objects.get(id=teamid)
    except Team.DoesNotExist:
        return {'ret': 1, 'msg': f'id 为`{teamid}`的队伍不存在'}

    if 'team_name' in newdata:
        team.team_name = newdata['team_name']
    if 'coach' in newdata:
        team.coach = newdata['coach']
    if 'group' in newdata:
        team.group = newdata['group']
    if 'point' in newdata:
        team.point = newdata['point']

    # 注意，一定要执行save才能将修改信息保存到数据库
    team.save()

    return JsonResponse({'ret': 0})


def deleteteam(request):

    teamid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的队伍记录
        team = Team.objects.get(id=teamid)
    except Team.DoesNotExist:
        return {
                'ret': 1,
                'msg': f'id 为`{teamid}`的队伍不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    team.delete()

    return JsonResponse({'ret': 0})


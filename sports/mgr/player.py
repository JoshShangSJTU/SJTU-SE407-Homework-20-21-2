from django.http import JsonResponse
from splatform.models import Player
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
    if action == 'list_player':
        return listplayer(request)
    elif action == 'add_player':
        return addplayer(request)
    elif action == 'modify_player':
        return modifyplayer(request)
    elif action == 'del_player':
        return deleteplayer(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def listplayer(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Player.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})


def addplayer(request):

    info = request.params['data']

    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = Player.objects.create(
        player_name=info['player_name'],
        goal=info['goal'],
        assist=info['assist'],
        y_card=info['y_card'],
        r_card=info['r_card'],
        team=info['team'],
    )

    return JsonResponse({'ret': 0, 'id': record.id})


def modifyplayer(request):

    # 从请求消息中 获取修改客户的信息
    # 找到该客户，并且进行修改操作

    playerid = request.params['id']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        player = Player.objects.get(id=playerid)
    except player.DoesNotExist:
        return {'ret': 1, 'msg': f'id 为`{playerid}`的客户不存在'}

    if 'player_name' in newdata:
        player.player_name = newdata['player_name']
    if 'goal' in newdata:
        player.goal = newdata['goal']
    if 'assist' in newdata:
        player.assist = newdata['assist']
    if 'y_card' in newdata:
        player.y_card = newdata['y_card']
    if 'r_card' in newdata:
        player.r_card = newdata['r_card']
    if 'team' in newdata:
        player.team = newdata['team']

    # 注意，一定要执行save才能将修改信息保存到数据库
    player.save()

    return JsonResponse({'ret': 0})


def deleteplayer(request):

    playerid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        player = Player.objects.get(id=playerid)
    except player.DoesNotExist:
        return {
                'ret': 1,
                'msg': f'id 为`{playerid}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    player.delete()

    return JsonResponse({'ret': 0})


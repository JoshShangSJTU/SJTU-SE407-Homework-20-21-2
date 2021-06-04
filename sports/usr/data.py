from django.contrib.auth.models import User
from django.http import JsonResponse,HttpRequest
from django.contrib.auth import authenticate, login



def data(request):
    if 'usertype' not in request.session:
        return JsonResponse({'ret': 1,'msg': '未登录'})
    else:
        return JsonResponse(
            {
                'ret':0,
                'usertype': request.session['usertype'],
                'username': request.user.username,
                'useremail': request.user.email
            }
        )
    
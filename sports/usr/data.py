from django.contrib.auth.models import User
from django.http import JsonResponse,HttpRequest
from django.contrib.auth import authenticate, login



def data(request):
    if 'usertype' not in request.session:
        return JsonResponse({'ret': 1,'msg': '未登录'})
    else:
        userName=HttpRequest.user.get_username()
        userEmail=HttpRequest.user.get_useremail()
        return JsonResponse(
            {
                'ret':0,
                'usertype': request.session['usertype'],
                'username': userName,
                'useremail': userEmail
            }
        )
    
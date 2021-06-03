from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
import json

def register(request):

    request_data = json.loads(request.body)
    userName = request_data["username"]
    userexist = authenticate(username=userName)
    if userexist is not None:
        return JsonResponse({'ret': 1, 'msg': '用户名已存在'})
    passWord = request_data["password"]
    passWord2 = request_data["password2"]
    Email = request_data["email"]

    if not passWord == passWord2:
        return JsonResponse({'ret': 1, 'msg': '两次密码不一致'})
    user = User.objects.create_user(username=userName, password=passWord, email=Email)
    user.save()
    userlogin = authenticate(username=userName, password=passWord)
    login(request,userlogin)
    request.session['usertype'] = 'usr'
    request.session['username'] = userName
    return JsonResponse({'ret': 0})


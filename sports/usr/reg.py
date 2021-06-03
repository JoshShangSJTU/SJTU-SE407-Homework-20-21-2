from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

def register(request):

    userName = request.POST.get('username')
    #userexist = authenticate(username=userName)
   #if userexist is not None:
    #    return JsonResponse({'ret': 1, 'msg': '用户名已存在'})
    passWord = request.POST.get('password')
    passWord2 = request.POST.get('password2')
    Email = request.POST.get('email')
    return {'ret': 0}

    #if not passWord == passWord2:
    #    return JsonResponse({'ret': 1, 'msg': '两次密码不一致'})
    #user = User.objects.create_user(username=userName, password=passWord, email=Email)
    #user.save()
    #userlogin = authenticate(username=userName, password=passWord)
    #login(request,userlogin)
    #request.session['usertype'] = 'usr'
    #return {'ret': 0}


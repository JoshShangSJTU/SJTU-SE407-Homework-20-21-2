from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

def register(request):

    if not request.POST.get('username'):
        return JsonResponse({'ret': 1, 'msg': '用户名不能为空'})
    userName = request.POST.get('username')
    userexist = authenticate(username=userName)
    if userexist is not None:
        return JsonResponse({'ret': 1, 'msg': '用户名已存在'})

    if not request.POST.get('password'):
        return JsonResponse({'ret': 1, 'msg': '密码不能为空'})
    passWord = request.POST.get('password')

    
    if not request.POST.get('password2'):
        return JsonResponse({'ret': 1, 'msg': '确认密码不能为空'})
    passWord2 = request.POST.get('password2')

    if not request.POST.get('email'):
        return JsonResponse({'ret': 1, 'msg': '邮箱不能为空'})
    Email = request.POST.get('email')


    if passWord is not None:
        if not passWord == passWord2:
            return JsonResponse({'ret': 1, 'msg': '两次密码不一致'})

    if userName is not None and Email is not None : 
        user = User.objects.create_user(userName, Email, passWord)
        user.save()
        userlogin = authenticate(username=userName, password=passWord)
        login(request,userlogin)
        request.session['usertype'] = 'usr'
        return {'ret': 0}


from django.shortcuts import render
from django.http.response import HttpResponse


from splatform import models
# Create your views here.

def Login(request):
    #输入用户名提交后返回"hello,用户名"
    if request.method == "POST":
        username = request.POST.get('username')
        return HttpResponse("hello,"+username)
    else:#初始登录时返回一个静态登录页面
        return render(request,'home.html')

def QueryPlayers(request):
    players = models.Player.objects.all() 
    print(players,type(players)) # QuerySet类型，类似于list，访问 url 时数据显示在命令行窗口中。
    return HttpResponse("<p>查找成功！</p>")
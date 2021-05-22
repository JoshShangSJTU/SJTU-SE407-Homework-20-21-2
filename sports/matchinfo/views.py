from django.shortcuts import render
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def POSTtest(request):
    if request.method == 'POST':
        return("收到POST请求")
    else:
        return("未收到POST请求")

@csrf_exempt
def Login(request):
    #输入用户名提交后返回"hello,用户名"
    if request.method == "POST":
        username = request.POST.get('username')
        return HttpResponse("hello,"+username)
    else:#初始登录时返回一个静态登录页面
        return render(request,'home.html')
from django.shortcuts import render

# Create your views here.

def POSTtest(request):
    if request.method == 'POST':
        return("收到POST请求")
    else:
        return("未收到POST请求")
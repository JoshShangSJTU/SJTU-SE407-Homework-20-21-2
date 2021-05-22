from django.shortcuts import render
from django.http.response import HttpResponse



from splatform import models
# Create your views here.

'''
查询语法：
.all()  选择全部对象
.filter()   筛选符合括号内筛选条件的对象
    如：    models.Book.objects.filter(pk=5)
    pk为primary key，代表数据库中的id

.exclude() 筛选不符合括号内筛选条件的对象
.get()      筛选对象，且只能返回一个对象，否则报错
.order_by() 方法用于对查询结果进行排序
    a、参数的字段名要加引号。
    b、降序为在字段前面加个负号 -。
        如：    models.Book.objects.order_by(-"price")

count() 方法用于查询数据的数量，返回的数据是整数

'''

def Login(request):
    #输入用户名提交后返回"hello,用户名"
    if request.method == "POST":
        username = request.POST.get('username')
        return HttpResponse("hello,"+username)
    else:#初始登录时返回一个静态登录页面
        return render(request,'home.html')

def QueryPlayers(request):
    package = []
    #player_count = models.Player.objects.all().count() 

   
    for player in models.Player.objects.all():
        exec('player{}={}'.format(player.pk, player.pk))
        exec('print(player{})'.format(player.pk))
        exec('package.append(player{})'.format(player.pk))
        print(package)
    
    return HttpResponse("<p>查找成功！</p>")

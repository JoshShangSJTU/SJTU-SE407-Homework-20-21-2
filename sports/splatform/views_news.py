from .models import News
from django.shortcuts import redirect 
from django.forms.models import model_to_dict



def news_list(request):
    global url_dict

    if request.method == 'GET':
        num1 = request.GET.get('num')
        url = News.objects.filter(num = num1).first()
        url_dict = {
            'num': url.num,
            'url': url.url
        }
        

    return redirect(url_dict['url'])
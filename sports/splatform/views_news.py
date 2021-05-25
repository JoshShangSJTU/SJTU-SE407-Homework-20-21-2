from .models import News
from django.shortcuts import redirect 

def news_list(request):
    if request.method == 'POST':
        r_id = request.POST.get('num')
        url = News.objects.filter(num = r_id).values()['url']
    return redirect(url)
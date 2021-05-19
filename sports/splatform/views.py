from django.http.response import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from .models import Player
from django.shortcuts import render

class HomeView(TemplateView):
    template_name = "home.html"

    def goal_list(request):
        if request.method == 'GET':
            results = Player.objects.order_by('-goal')
            for i in results:
                data = {}
                data['name'] = i.player_name
                data['team'] = i.team
                data['goal'] = i.goal
            return JsonResponse({'status':200, 'data':data})

    
    
    



from django.views.generic import TemplateView
from .models import Player
from django.shortcuts import render

class HomeView(TemplateView):
    template_name = "home.html"

    def goal_list(request):
        players = {}
        players = Player.objects.order_by('-goal')
        return render(request, 'home.html', players)

    



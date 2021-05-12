from django.views.generic import TemplateView
from .models import Player

class HomeView(TemplateView):
    template_name = "home.html"

    def score_list(request):
        players = Player.objects.order_by("-goal")
        return players



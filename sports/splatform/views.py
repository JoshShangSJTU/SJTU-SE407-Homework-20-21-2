from django.http.response import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from .models import Player
from django.shortcuts import render
from django.forms.models import model_to_dict  

class HomeView(TemplateView):
    template_name = "home.html"

    def goal_list(request):
        results = Player.objects.order_by('-goal')
        result_dict = model_to_dict(results)

        return render(request, 'home.html', result_dict)
    
    
    



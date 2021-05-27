from django.http.response import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from .models import Player
from django.shortcuts import render
from django.forms.models import model_to_dict  

def goal_list(request):
    if request.method() == "GET":
        results = Player.objects.order_by('-goal')
        result_dict = model_to_dict(results)

        return JsonResponse({'status':200, 'data':result_dict})


    
    
    



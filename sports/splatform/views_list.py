from django.http.response import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from .models import Player
from django.shortcuts import render
from django.forms.models import model_to_dict  

def goal_list(request):
    
   results = Player.objects.order_by('-goal')
   dict_test = {'status': 'test'}
   return render(request, 'home.html', context=dict_test)


    
    
    



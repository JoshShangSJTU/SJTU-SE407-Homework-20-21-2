from django.urls import path
from django.views.generic.base import TemplateView


urlpatterns = [

    path('home',TemplateView.as_view(template_name='home_match.html')),

]
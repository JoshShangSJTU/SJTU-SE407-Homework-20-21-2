from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [

    path('home/',TemplateView.as_view(template_name='home_match.html')),
    path('home/login/', TemplateView.as_view(template_name='login.html')),
    path('match-detail',TemplateView.as_view(template_name='match_detail.html')),
    path('Query',views.Query)

]
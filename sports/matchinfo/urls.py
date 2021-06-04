from django.urls import path, re_path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    # 页面路径
    path('home/',TemplateView.as_view(template_name='home_match.html')),
    path('home/login/', TemplateView.as_view(template_name='login.html')),
    path('home/match-detail',TemplateView.as_view(template_name='match_detail.html')),
    re_path(r'^home/match-detail/(\-?)(\d+)/$',TemplateView.as_view(template_name='match_detail.html')),
    

    #api路径
    path('api/homedata/',views.Homedata),
    re_path(r'api/homedata/(?P<page>\d+)/$',views.Homedata),
    path('api/detaildata/',views.Detaildata),
    re_path(r'^api/detaildata/(?P<sign>\-?)(?P<para>\d+)/$', views.Detaildata)

]
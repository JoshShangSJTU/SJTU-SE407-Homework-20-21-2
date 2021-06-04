from django.urls.resolvers import URLPattern
from django.conf.urls import url, include
from django.urls import path, re_path
from rest_framework import routers

from . import views

urlpatterns = [
    url('goal_list', views.GoalListAPIView.as_view(), name='goal_list'),
]
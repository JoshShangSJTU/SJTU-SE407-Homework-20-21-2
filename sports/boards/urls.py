from .models import Topic
from django.conf.urls import url, include
from django.urls import path, re_path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('boards', views.BoardViewSet)
router.register('post', views.PostViewSet)

urlpatterns = [
    path('', views.BoardListView.as_view(), name='home_boards'),
    re_path(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
    re_path(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='edit_post'),
    
    # 这是boards的api接口
    path('api/', include(router.urls)),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
]
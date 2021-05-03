from django.conf.urls import url, include
from django.urls import path

from . import views


urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
    path(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),
    path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),
    path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='edit_post'),
]
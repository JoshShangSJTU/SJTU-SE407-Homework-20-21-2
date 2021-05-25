# 这是序列化文件
from django.db.models import fields
from django.forms.models import model_to_dict
from .models import Board, Topic, Post
from rest_framework import serializers

class BoardSerializer(serializers.ModelSerializer):
    '''
    Board序列化
    '''
    class Meta:
        model = Board
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    '''
    Topic序列化
    '''
    class Meta:
        model = Topic
        fields = ('id', 'subject', 'last_updated', 'board', 'starter', 'views')
        

class PostListSerializer(serializers.ModelSerializer):
    '''
    Post序列化
    '''
    class Meta:
        model = Post
        fields = '__all__'

# 这是序列化文件
from django.db.models import fields
from .models import Board, Topic, Post
from rest_framework import serializers

class BoardSerializer(serializers.ModelSerializer):
    '''
    区域信息序列化
    '''
    class Meta:
        model = Board
        fields = '__all__'
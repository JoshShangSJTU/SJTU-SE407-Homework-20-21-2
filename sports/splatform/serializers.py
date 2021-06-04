# 这是序列化文件
from django.db.models import fields
from django.utils import timezone

from rest_framework import serializers

from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    '''
    Player序列化
    '''

    class Meta:
        model = Player
        fields = ('player_name', 'goal')
    
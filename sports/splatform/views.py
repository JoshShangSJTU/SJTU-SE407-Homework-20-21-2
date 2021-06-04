from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, query
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse, Http404

from rest_framework import viewsets, mixins
from rest_framework import generics
from rest_framework import pagination
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer, Serializer
from rest_framework.decorators import action
from rest_framework import status

from .models import Match, Player, Team
from .serializers import PlayerSerializer

class GoalListAPIView(generics.ListAPIView):
    '''
    射手榜信息展示api
    '''
    def get_queryset(self, *args, **kwargs):
        try:
            queryset = Player.objects.order_by('-goal').values('player_name', 'team', 'goal')
            return queryset
        except self.board.DoesNotExist:
            raise Http404
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PlayerSerializer(queryset, many=True)
        return Response(serializer.data)        
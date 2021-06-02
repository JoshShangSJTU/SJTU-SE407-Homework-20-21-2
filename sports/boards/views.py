from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, query
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets, mixins
from rest_framework import generics
from rest_framework import pagination
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.decorators import action

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm
from .serializers import BoardSerializer, TopicSerializer, PostListSerializer


# Create your views here.
# 下面是接口
# class BoardList(generics.ListAPIView):
#     """
#     Board展示
#     """
#     queryset = Board.objects.all()
#     serializer_class = BoardSerializer

class BoardViewSet(viewsets.ModelViewSet, mixins.ListModelMixin):
    """
    Board的视图集
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10000
    page_query_param = 'p'

class TopicListAPIView(generics.ListAPIView):
    """
    Topic展示
    """
    def get(self, request, *args, **kwargs):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated')
        paginator = CustomPagination()
        result = paginator.paginate_queryset(queryset, request)
        serializer = TopicSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)
    
class PostListAPIView(generics.ListAPIView):
    """
    Post展示
    """
    def get(self, request, *args, **kwargs):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        paginator = CustomPagination()
        result = paginator.paginate_queryset(queryset, request)
        serializer = PostListSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)


class PostUpadateAPIView(generics.UpdateAPIView):
    '''
    编辑post
    '''
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

class PostDeleteAPIView(generics.DestroyAPIView):
    '''
    删除post
    '''
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

# class TopicViewSet(viewsets.ModelViewSet):
#     serializer_class = TopicSerializer
#     pagination_class = CustomPagination

#     def get_object(self):
#         return get_object_or_404(Board, pk=self.request.query_params.get('pk'))

#     def get_queryset(self):
#         return Board.topics.order_by('-last_updated')

#     def perform_destroy(self, instance):
#         instance.is_active = False
#         instance.save()

# class BoardViewSet(viewsets.ModelViewSet, mixins.ListModelMixin):
#     """
#     Board的视图集
#     """
#     queryset = Board.objects.all()
#     serializer_class = BoardSerializer
    
#     # 展示Topics
#     @action(methods=['get'], pagination_class = LimitOffsetPagination, permission_classes=[AllowAny], detail=True, url_path=r'topics/(?P<topic_pk>\d+)')
#     def showTopic(self, request, *args, **kwargs):
#         self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
#         queryset = self.board.topics.order_by('-last_updated')
#         serializer = TopicSerializer(queryset, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     # 展示Posts
#     @action(methods=['get'], pagination_class = LimitOffsetPagination, permission_classes=[AllowAny], detail=True, url_path=r'topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)')
#     def showPost(self, request, *args, **kwargs):
#         self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
#         queryset = self.topic.posts.order_by('created_at')
#         serializer = PostListSerializer(queryset, many=True)
#         return JsonResponse(serializer.data, safe=False)


# class TopicViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, viewsets.ViewSet):
#     '''
#     Topic的视图集
#     '''
#     def list(self, request, *args, **kwargs):
#         self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
#         queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
#         serializer = TopicSerializer(queryset, many=True)
#         return Response(serializer.data)
#     # queryset = Topic.objects.all().order_by('-last_updated').annotate(replies=Count('posts') - 1)
#     # serializer_class = TopicSerializer
#     pagination_class = LimitOffsetPagination
#     permission_classes = [AllowAny]


# class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     '''
#     Post的视图集
#     '''
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer
#     permission_classes = [AllowAny]



# -----------------这是分割线-----------------------
# 下面的是原来的view函数，上面的部分是在返回api，目前
# 等待前端同学完善
# 下面的部分目前还在使用中，前后端分离尚未分离
# ----------------这是分割线------------------------
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home_boards.html'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(
            replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):

        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic,
                                       board__pk=self.kwargs.get('pk'),
                                       pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user,
            )
            return redirect('topic_posts', pk=pk,
                            topic_pk=topic.pk)  # 重定向回新建的topic页面
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts',
                        pk=post.topic.board.pk,
                        topic_pk=post.topic.pk)

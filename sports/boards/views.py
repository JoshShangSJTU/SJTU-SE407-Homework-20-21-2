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

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm
from .serializers import BoardSerializer, TopicSerializer, PostSerializer

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


class MyPagination(PageNumberPagination):
    page_size = 4  # 每页4条（默认）
    max_page_size = 50  # 最大每页条数（根据传入的值分页）
    page_query_param = "page"  # 前端url中传入的‘页数’名字
    page_size_query_param = "page_size"  # 前端url中传入的每页的数据条数


class TopicListAPIView(generics.ListAPIView):
    """
    Topic展示
    """
    def get_queryset(self, *args, **kwargs):
        try:
            self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
            queryset_list = self.board.topics.order_by('-last_updated')
            return queryset_list
        except self.board.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = MyPagination()
        result = paginator.paginate_queryset(queryset, request, self)
        serializer = TopicSerializer(result, many=True)
        data = {
            'count': queryset.count(),  # 获取数据总数
            'previous': paginator.get_previous_link(),  # 获取上一页链接，如果没有则是None
            'next': paginator.get_next_link(),  # 获取下一页链接，如果没有则是None
            'results': serializer.data,  # 当前页的序列化数据
        }
        return Response(data)


class PostListAPIView(generics.ListAPIView):
    """
    Post展示
    """
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        try:
            self.topic = get_object_or_404(Topic,
                                           board__pk=self.kwargs.get('pk'),
                                           pk=self.kwargs.get('topic_pk'))
            queryset_list = self.topic.posts.order_by('created_at')
            return queryset_list
        except self.topic.DoesNotExist:
            return Http404

    def get(self, request, *args, **kwargs):
        result = self.get_queryset()
        serializer = PostSerializer(result, many=True)
        return Response(serializer.data)


class PostUpdateAPIView(generics.UpdateAPIView):
    '''
    编辑post
    '''
    serializer_class = PostSerializer

    def get_queryset(self, *args, **kwargs):
        self.topic = get_object_or_404(Topic,
                                       board__pk=self.kwargs.get('pk'),
                                       pk=self.kwargs.get('topic_pk'))
        queryset_list = self.topic.posts.order_by('created_at')
        return queryset_list

    def patch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        serializer = PostSerializer(data=request.data,
                                    instance=post,
                                    partial=True)
        if serializer.is_valid():
            serializer.updated_at = timezone.now()
            serializer.updated_by = self.request.user
            post = serializer.save()
            return Response(PostSerializer(post).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDeleteAPIView(generics.DestroyAPIView):
    '''
    删除Post
    '''
    serializer_class = PostSerializer

    def get_object(self):
        board_pk = self.kwargs.get('pk')
        topic_pk = self.kwargs.get('topic_pk')
        post_pk = self.kwargs.get('post_pk')
        return Post.objects.get(post_pk=post_pk)

    def get_queryset(self, *args, **kwargs):
        self.topic = get_object_or_404(Topic,
                                       board__pk=self.kwargs.get('pk'),
                                       pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

    def get_object(self):
        self.pk = self.kwargs.get('pk')
        self.topic_pk = self.kwargs.get('topic_pk')
        self.post_pk = self.kwargs.get('post_pk')
        query = self.get_queryset()
        obj = query.filter(id=self.post_pk)
        return obj

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

            topic_url = reverse('topic_posts',
                                kwargs={
                                    'pk': pk,
                                    'topic_pk': topic_pk
                                })
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url, id=post.pk, page=topic.get_page_count())

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

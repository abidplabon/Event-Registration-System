from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from App_Posts.models import Post, Like
from App_Login.models import Follow
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import PostSerializer, LikeSerializer


# Create your views here.

@login_required
def home(request):
    following_list = Follow.objects.filter(follower=request.user)
    posts = Post.objects.filter(author__in=following_list.values_list('following'))
    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list('post', flat=True)

    if request.method == 'GET':
        search = request.GET.get('search', '')
        user_results = User.objects.filter(username__icontains=search)
        post_results = Post.objects.filter(Q(event_title__icontains=search) | Q(location__icontains=search))

    return render(request, 'App_Posts/home.html', {
        'title': 'Home Page',
        'search': search,
        'user_results': user_results,
        'post_results': post_results,
        'posts': posts,
        'liked_post_list': liked_post_list
    })


@login_required
def liked(request, pk):
    post = get_object_or_404(Post, pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user).exists()

    if not already_liked:
        liked_post = Like(post=post, user=request.user)
        liked_post.save()
        post.likes += 1  # Increment the likes count
        post.save()

    return HttpResponseRedirect(reverse('home'))


@login_required
def unliked(request, pk):
    post = get_object_or_404(Post, pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user).exists()

    if already_liked:
        Like.objects.filter(post=post, user=request.user).delete()
        post.likes -= 1  # Decrement the likes count
        post.save()

    return HttpResponseRedirect(reverse('home'))


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked = post.pk in Like.objects.filter(user=request.user).values_list('post', flat=True)
    return render(request, 'App_Posts/post_detail.html', {'post': post, 'liked': liked})


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


class LikeListAPIView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [AllowAny]


class LikeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [AllowAny]

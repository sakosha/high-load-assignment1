from typing import TYPE_CHECKING

# from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import CommentForm
from .forms import PostForm
from .forms import SignUpForm
from .models import Post

if TYPE_CHECKING:
    from django.http import HttpRequest

    from .models import Comment


def signup(request: 'HttpRequest') -> HttpResponse:
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def index(request: 'HttpRequest'):  # noqa: ARG001
    return HttpResponse('Hello, Blog!')


def post_list(request: 'HttpRequest') -> HttpResponse:
    posts = Post.objects.all()

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    post_page = paginator.get_page(page)

    return render(request, 'blog/post_list.html', {'posts': post_page})


def post_detail(request: 'HttpRequest', pk: int) -> HttpResponse:
    post = Post.objects.get(pk=pk)

    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment: Comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(
        request,
        'blog/post_detail.html',
        {'post': post, 'comments': comments, 'comment_form': comment_form},
    )


@login_required
def post_new(request: 'HttpRequest') -> HttpResponse:
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post: Post = form.save(commit=False)  # to assign to None fields
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})


@login_required
def post_edit(request: 'HttpRequest', pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        raise PermissionDenied

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})


@login_required
def post_delete(request: 'HttpRequest', pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        raise PermissionDenied

    post.delete()
    return redirect('post_list')

# ruff: noqa: ARG001

# Create your views here.
from typing import TYPE_CHECKING

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import CommentForm
from .forms import PostForm
from .models import Post

if TYPE_CHECKING:
    from django.http import HttpRequest


def home(request: 'HttpRequest') -> HttpResponse:
    return HttpResponse('Hello, Blog!')


def post_list(request: 'HttpRequest') -> HttpResponse:
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'post_list.html', {'page_obj': page_obj})


def post_detail(request: 'HttpRequest', post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)  # type: ignore[attr-defined]
    return render(
        request, template_name='post_detail.html', context={'post': post}
    )


@login_required
def post_create(request: 'HttpRequest') -> HttpResponse:
    if request.method == 'POST':  # noqa: PLR2004
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(
        request, template_name='create_post.html', context={'form': form}
    )


@login_required
def post_edit(request: 'HttpRequest', post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)  # type: ignore[attr-defined]
    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':  # noqa: PLR2004
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)  # type: ignore[attr-defined]
    else:
        form = PostForm(instance=post)
    return render(
        request, template_name='post_edit.html', context={'form': form}
    )


@login_required
def post_delete(request: 'HttpRequest', post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)  # type: ignore[attr-defined]
    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':  # noqa: PLR2004
        post.delete()
        return redirect('post_list')
    return render(
        request=request,
        template_name='post_confirm_delete.html',
        context={'post': post},
    )


def add_comment_to_post(request: 'HttpRequest', post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)  # type: ignore[attr-defined]
    if request.method == 'POST':  # noqa: PLR2004
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)  # type: ignore[attr-defined]
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})


def signup(request: 'HttpRequest') -> HttpResponse:
    if request.method == 'POST':  # noqa: PLR2004
        form = UserCreationForm(request.POST)
        if form.is_valid():
            _ = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

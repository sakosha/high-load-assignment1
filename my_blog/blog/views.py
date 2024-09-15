from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .models import Post
from .forms import PostForm


def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello, Blog!')


def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all()
    return render(request=request, template_name='post_list.html', context={'posts': posts})


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    return render(request=request, template_name='post_list.html', context={'post': post})


def create_post(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request=request, template_name='create_post.html', context={'form': form})

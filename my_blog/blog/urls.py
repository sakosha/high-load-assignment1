from django.urls import include
from django.urls import path

from .views import index
from .views import post_detail
from .views import post_edit
from .views import post_list
from .views import post_new
from .views import signup

urlpatterns = [
    # path('', index, name='index'),
    path('', post_list, name='post_list'),
    path('post/new/', post_new, name='post_create'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', post_edit, name='post_edit'),
    path('signup/', signup, name='signup'),
    path('', include('django.contrib.auth.urls')),
]

from django.urls import path
from .views import PostViewSet, UserViewSet, CommentViewSet, TagviewSet

urlpatterns = [
    path('posts', PostViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='create_or_get_alL_posts'),
    path('posts/<str:pk>', PostViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='get_certain_post'),
    # all comments from post
    path('posts/<str:pk>/comments', PostViewSet.as_view({
        'get': 'get_comments'
    })),
    path('add_comments/<str:pk>', CommentViewSet.as_view({
        'post': 'create'
    }), name='create_comment'),
    path('posts/<str:pk>/comments_number', PostViewSet.as_view({
        'get': 'get_number_of_comments'
    })),
    path('comments/<str:pk>', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('posts/tags/', PostViewSet.as_view({
        'get': 'get_all_posts_number'
    })),
    path('posts/tags/number/', PostViewSet.as_view({
        'get': 'get_number_of_posts_by_tag'
    })),
    path('comments', CommentViewSet.as_view({
        'get': 'list'
    }), name='get_all_comments'),
    path('users', UserViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='user_create_or_get_all'),
    path('users/<str:pk>', UserViewSet.as_view({
        'get': 'retrieve'
    })),
    path('users_check_credentials/', UserViewSet.as_view({
        'get': 'check_credentials'
    })),
    path('tags', TagviewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='tag_create_or_get_all'),
    path('tags/<str:pk>', TagviewSet.as_view({
        'delete': 'destroy',
        'get': 'retrieve'
    }))
]

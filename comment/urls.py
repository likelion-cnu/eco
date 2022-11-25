from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve
from django.urls import re_path
from django.conf import settings

from . import views


user_list = views.PostViewSet.as_view({'get': 'retrieve'})

comment_list = views.CommentViewSet.as_view({'get': 'list', 'post': 'create'})

urlpatterns = [
    path("home/", user_list, name="root"), # 홈화면 조회
    path("home/<str:post>/", views.EmotionViewSet.as_view(), name="profile"), # 재난별 페이지
    path("home/<str:post>/sad", views.sad_add, name="sad"), # 슬픈 감정 추가
    path("home/<str:post>/surprise", views.surprise_add, name="comment"), # 놀란 감정 추가
    path("home/<str:post>/angry", views.angry_add, name="comment"), # 화난 감정 추가
    path("home/<str:post>/comment", comment_list, name="sad"), # 댓글 조회, 추가

	re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
]
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve
from django.urls import re_path
from django.conf import settings

from . import views


user_list = views.PostViewSet.as_view({'get': 'list'})


urlpatterns = [
    path("home/", user_list, name="root"), # 홈화면 조회
    path("home/<str:post>", views.detail_view, name="profile"), # 재난별 페이지
    path("home/<str:post>/sad", views.sad_add, name="sad"), # 슬픈 감정 추가
    path("home/<str:post>/surprise", views.surprise_add, name="surprise"), # 놀란 감정 추가
    path("home/<str:post>/angry", views.angry_add, name="angry"), # 화난 감정 추가
    path('home/<str:post>/comments', views.comments_view, name='comment_list_get'),
    path('home/<str:post_pk>/comments/<int:comment_pk>', views.comment_detail_update_delete, name='comment_list_get'),
    path('home/<str:post>/add/comments', views.PostCommentViewSet.as_view(), name='comment_list_create'),

	re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
]
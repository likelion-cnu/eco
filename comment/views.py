from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView 
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination # 👈 페이지 기반 파지네이션 import


# Create your views here.
from .serializers import PostSerializer, EmotionSerializer, SadEmotionSerializer, SurpriseEmotionSerializer, AngryEmotionSerializer, CommentSerializer
from .models import Post, Comment, Emotion

class Pagination(PageNumberPagination): # 👈 PageNumberPagination 상속
    page_size = 20


# 홈 화면
class PostViewSet(ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = Pagination


# 재난별 페이지
class EmotionViewSet(RetrieveAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer

    lookup_field = 'post'


# 슬퍼요 누르는 버튼 // 추후 쿠키를 사용한 중복 방지 구현하기
@api_view(['GET'])
def sad_add(request, post):
    sad = Emotion.objects.get(post=post)
    sad.sad_cnt += 1
    sad.save()
    
    serializer = SadEmotionSerializer(sad)
    return Response(serializer.data, status=201)


# 놀랐어요 누르는 버튼 // 추후 쿠키를 사용한 중복 방지 구현하기
@api_view(['GET'])
def surprise_add(request, post):
    surprise = Emotion.objects.get(post=post)
    surprise.surprise_cnt += 1
    surprise.save()
    
    serializer = SurpriseEmotionSerializer(surprise)
    return Response(serializer.data, status=201)


# 화났어요 누르는 버튼 // 추후 쿠키를 사용한 중복 방지 구현하기
@api_view(['GET'])
def angry_add(request, post):
    angry = Emotion.objects.get(post=post)
    angry.sad_cnt += 1
    angry.save()
    
    serializer = AngryEmotionSerializer(angry)
    return Response(serializer.data, status=201)


# 댓글 조회, 추가
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = Pagination

    lookup_field = 'post'

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['post'])
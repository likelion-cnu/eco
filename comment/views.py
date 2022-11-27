import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView 
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination # 👈 페이지 기반 파지네이션 import
from django.core.exceptions import ObjectDoesNotExist

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
    

# 재난별 페이지를 
@api_view(['GET']) # 중복 생성 안되게
def detail_view(request, post):
    try: # when
        detail = Emotion.objects.get(post=post)
        
    except ObjectDoesNotExist: # 에러가 생긴다면
        Post(post_pk=post).save()
        n_post = Post.objects.get(post_pk=post)
        
        Emotion(post=n_post).save()
        Comment(post=n_post).save()
        
        new_post = Emotion.objects.get(post=post)
        serializer = EmotionSerializer(new_post)
        return Response(serializer.data, status=201)
    
    else: # 에러가 생기지 않는다면
        new_post = Emotion.objects.get(post=post)
        serializer = EmotionSerializer(new_post)
        return Response(serializer.data, status=201)



# 슬퍼요 누르는 버튼 // 추후 쿠키를 사용한 중복 방지 구현하기
@api_view(['POST'])
def sad_add(request, post):
    if request.method == 'POST':     
        sad = Emotion.objects.get(post=post)
        sad.sad_cnt += 1
        sad.save()
    
        serializer = SadEmotionSerializer(sad)
        return Response(serializer.data, status=201)


# 놀랐어요 누르는 버튼 // 추후 쿠키를 사용한 중복 방지 구현하기
@api_view(['POST'])
def surprise_add(request, post):
    if request.method == 'POST':
        surprise = Emotion.objects.get(post=post)
        surprise.surprise_cnt += 1
        surprise.save()
        
        serializer = SurpriseEmotionSerializer(surprise)
        return Response(serializer.data, status=201)


# 화났어요 누르는 버튼 // 추후 쿠키를 사용한 중복 방지 구현하기
@api_view(['POST'])
def angry_add(request, post):
    if request.method == 'POST':
        angry = Emotion.objects.get(post=post)
        angry.angry_cnt += 1
        angry.save()
        
        serializer = AngryEmotionSerializer(angry)
        return Response(serializer.data, status=201)


# 댓글 조회
class ReadCommentViewSet(ReadOnlyModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = Pagination
    
    lookup_field = 'post'
    
    def get_queryset(self):
        post = Post.objects.get(post_pk=self.kwargs.get('post'))
        qs = super().get_queryset()
        qs = qs.filter(post = post)
        return qs
    
    
# 댓글 업데이트, 삭제
@api_view(['GET','PUT','DELETE'])
def comment_detail_update_delete(request, post_pk, comment_pk): 
    
    comment = get_object_or_404(Comment, pk=comment_pk, post=post_pk)
    
    if request.method=='GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    elif request.method =='DELETE':
        comment.delete()
        return Response({'comment_pk':comment_pk},status=204)
    
    elif request.method=='PUT':
        serializer=CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data,status=200)

    
# 댓글 생성하기
class PostCommentViewSet(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    lookup_field = 'post'

    def get_queryset(self):
        post = Post.objects.get(post_pk=self.kwargs.get('post'))
        qs = super().get_queryset()
        qs = qs.filter(post = post)
        return qs
    
    def perform_create(self, serializer):
        serializer.save(post=Post.objects.get(post_pk=self.kwargs.get('post')))

    
    
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView 
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination # π νμ΄μ§ κΈ°λ° νμ§λ€μ΄μ import
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from .serializers import PostSerializer, EmotionSerializer, SadEmotionSerializer, SurpriseEmotionSerializer, AngryEmotionSerializer, CommentSerializer
from .models import Post, Comment, Emotion

class Pagination(PageNumberPagination): # π PageNumberPagination μμ
    page_size = 20


# ν νλ©΄
class PostViewSet(ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = Pagination
    

# μ¬λλ³ νμ΄μ§λ₯Ό 
@api_view(['GET']) # μ€λ³΅ μμ± μλκ²
def detail_view(request, post):
    try: # when
        detail = Emotion.objects.get(post=post)
        
    except ObjectDoesNotExist: # μλ¬κ° μκΈ΄λ€λ©΄
        Post(post_pk=post).save()
        n_post = Post.objects.get(post_pk=post)
        
        Emotion(post=n_post).save()
        Comment(post=n_post).save()
        
        new_post = Emotion.objects.get(post=post)
        serializer = EmotionSerializer(new_post)
        return Response(serializer.data, status=201)
    
    else: # μλ¬κ° μκΈ°μ§ μλλ€λ©΄
        new_post = Emotion.objects.get(post=post)
        serializer = EmotionSerializer(new_post)
        return Response(serializer.data, status=201)



# μ¬νΌμ λλ₯΄λ λ²νΌ // μΆν μΏ ν€λ₯Ό μ¬μ©ν μ€λ³΅ λ°©μ§ κ΅¬ννκΈ°
@api_view(['POST'])
def sad_add(request, post):
    if request.method == 'POST':     
        sad = Emotion.objects.get(post=post)
        sad.sad_cnt += 1
        sad.save()
    
        serializer = SadEmotionSerializer(sad)
        return Response(serializer.data, status=201)


# λλμ΄μ λλ₯΄λ λ²νΌ // μΆν μΏ ν€λ₯Ό μ¬μ©ν μ€λ³΅ λ°©μ§ κ΅¬ννκΈ°
@api_view(['POST'])
def surprise_add(request, post):
    if request.method == 'POST':
        surprise = Emotion.objects.get(post=post)
        surprise.surprise_cnt += 1
        surprise.save()
        
        serializer = SurpriseEmotionSerializer(surprise)
        return Response(serializer.data, status=201)


# νλ¬μ΄μ λλ₯΄λ λ²νΌ // μΆν μΏ ν€λ₯Ό μ¬μ©ν μ€λ³΅ λ°©μ§ κ΅¬ννκΈ°
@api_view(['POST'])
def angry_add(request, post):
    if request.method == 'POST':
        angry = Emotion.objects.get(post=post)
        angry.angry_cnt += 1
        angry.save()
        
        serializer = AngryEmotionSerializer(angry)
        return Response(serializer.data, status=201)


# λκΈ μ‘°ν -> api Viewλ‘ λ³κ²½νκΈ°
@api_view(['GET']) 
def comments_view(request, post):
    try: # when
        comments = Comment.objects.filter(post=post)
        
    except ObjectDoesNotExist: # μλ¬κ° μκΈ΄λ€λ©΄
        n_post = Post.objects.get(post_pk=post)
        Emotion(post=n_post).save()
        Comment(post=n_post).save()
        
        new_post = Comment.objects.filter(post=post)
        serializer = CommentSerializer(new_post, many=True)
        return Response(serializer.data, status=201)
    
    else: # μλ¬κ° μκΈ°μ§ μλλ€λ©΄
        new_post = Comment.objects.filter(post=post)
        serializer = CommentSerializer(new_post, many=True)
        return Response(serializer.data, status=201)


    
# λκΈ μλ°μ΄νΈ, μ­μ 
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

    
# λκΈ μμ±νκΈ°
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

    
    
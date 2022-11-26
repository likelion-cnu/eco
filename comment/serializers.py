from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Post, Comment, Emotion

# QR코드 Serializer
class PostSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('post_pk', 'comment')
        
    def get_comment(self, obj):
        cnt = Comment.objects.filter(post=obj.post_pk).count()
        return cnt


# QR코드 Serializer
class EmotionSerializer(serializers.ModelSerializer):
    # s_cnt = serializers.SerializerMethodField() # 슬픔
    # sur_cnt = serializers.SerializerMethodField() # 놀라움
    # ang_cnt = serializers.SerializerMethodField() # 화남
    
    class Meta:
        model = Emotion
        fields = ('sad_cnt', 'surprise_cnt', 'angry_cnt')
     

# 슬픈 감정 Serializer
class SadEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ('sad_cnt',)


# 놀란 감정 Serializer
class SurpriseEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ('surprise_cnt',)


# 화난 감정 Serializer
class AngryEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ('sad_cnt',)


# 댓글들 Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)
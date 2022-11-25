from django.db import models


class Post(models.Model): 
    post_pk = models.CharField(max_length=30, primary_key=True)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="Comment_Post")
    content = models.CharField(max_length=100)
    

class Emotion(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    sad_cnt = models.IntegerField(default=0)
    surprise_cnt = models.IntegerField(default=0)
    angry_cnt = models.IntegerField(default=0)
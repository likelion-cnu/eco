from django.contrib import admin
from .models import Post, Comment, Emotion

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Emotion)

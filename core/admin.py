from django.contrib import admin
from core.models import PostArticle

# Register your models here.

@admin.register(PostArticle)
class PostArticle(admin.ModelAdmin):
    list_display=('id','authorusername','title','desc','articleContent')

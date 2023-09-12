from django.db import models

# Create your models here.

class PostArticle(models.Model):
    authorusername = models.CharField(max_length=255)
    title=models.CharField(max_length=100)
    desc=models.CharField( max_length=300)
    articleContent=models.CharField(max_length=4000)
from datetime import timezone, datetime
from symtable import Class

from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models

# Create your media here.
class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class News(models.Model):
    class Status(models.TextChoices):
        Draft = 'DF', 'Draft'
        Published = 'PB', 'Published'

    #UUID = media.UUIDField(primary_key=True, unique=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to='news/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_time = models.DateTimeField(default=datetime.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices , default=Status.Draft)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_time']

    def get_absolute_url(self):
        return reverse('news_detail_page',args=[self.slug])


class Contacts(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    subject = models.CharField(max_length=150)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return self.email   

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta():
        ordering = ['created_time']

    def __str__(self):
        return f'comment: {self.body} created by {self.user}'
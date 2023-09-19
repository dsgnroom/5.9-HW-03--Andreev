from django.db import models
from django.db.models import Sum, Max
from django.contrib.auth.models import User
from news1.resources import POST_TYPES

class Author(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 0)

    def update_rating(self):
        rating = self.posts.all().aggregate(Sum('rating'))['rating__sum'] * 3 + Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum'] + Comment.objects.filter(post__author=self).aggregate(Sum('rating'))['rating__sum']
        self.rating=rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length = 128, unique = True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name='posts')
    type = models.CharField(max_length = 7, choices = POST_TYPES)
    creation_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length = 128)
    text = models.TextField()
    rating = models.IntegerField(default = 0)

    def preview(self):
        if len(self.text) < 125:
            shortcut = self.text
        else:
            shortcut = self.text[:124]+"..."
        return shortcut

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


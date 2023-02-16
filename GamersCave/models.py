from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Studio(models.Model):

    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(null=True)


class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)
    year = models.IntegerField()
    description = models.TextField()
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    rates = models.ManyToManyField(User, through="GameRating")

class GameRating(models.Model):
    RATES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7"),
        (8, "8"),
        (9, "9"),
        (10, "10"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=RATES)
    reviev = models.TextField(null=True)


class Article(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Forum_post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text=models.TextField()
    date= models.DateTimeField(auto_now_add=True)

class Post_answer(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Forum_post,on_delete=models.CASCADE,null=True)



from django.core.validators import MinValueValidator
from django.db import models


# user model
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=300)
    nickname = models.CharField(max_length=100)


class Tags(models.Model):
    text = models.CharField(primary_key=True, max_length=40)


# post model
class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=250)
    text = models.CharField(max_length=1000)
    # user foreign key
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    # tag foreign key
    tags = models.ManyToManyField(Tags)
    likes = models.IntegerField(validators=[MinValueValidator(0)],
                                blank=False, default=0)
    dislikes = models.IntegerField(validators=[MinValueValidator(0)],
                                   blank=False, default=0)


# comment model
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    user_id = models.ForeignKey(Users,
                                on_delete=models.CASCADE)
    likes = models.IntegerField(validators=[MinValueValidator(0)],
                                blank=False, default=0)
    dislikes = models.IntegerField(validators=[MinValueValidator(0)],
                                   blank=False, default=0)

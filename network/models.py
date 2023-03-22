from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    liked_posts = models.ManyToManyField('Post', verbose_name='Liked Posts', related_name='user_liked_posts', blank=True)
    followers = models.ManyToManyField('self', verbose_name='Followers', symmetrical=False, related_name='user_followers', blank=True)
    following = models.ManyToManyField('self', verbose_name='Following', symmetrical=False, related_name='user_following', blank=True)
    
    def get_followers(self):
        return self.user_followers.exclude(pk=self.pk)
    
    def get_following(self):
        return self.user_followers.exclude(pk=self.pk)

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=16, blank=False)
    post = models.TextField()
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user} posted {self.title} on {self.date}'
    
    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'user_id': self.user.pk,
            'title': self.title,
            'post': self.post,
            'likes': self.likes,
            'date': self.date.strftime('%Y-%m-%d')
        }


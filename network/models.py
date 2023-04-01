from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    liked_posts = models.ManyToManyField('Post', verbose_name='Liked Posts', related_name='user_liked_posts', blank=True)
    followers = models.ManyToManyField('self', verbose_name='Followers', symmetrical=False, related_name='user_followers', blank=True)
    following = models.ManyToManyField('self', verbose_name='Following', symmetrical=False, related_name='user_following', blank=True)
    slug = models.SlugField(null=True, unique=True)
    
    def get_followers(self):
        return self.followers.exclude(pk=self.pk)
    
    def get_following(self):
        return self.following.exclude(pk=self.pk)
    
    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"slug": self.slug})
    
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'followers': [follower.username for follower in self.get_followers().all()],
            'following': [following.username for following in self.get_following().all()],
            'followers_count': self.followers_count,
            'following_count': self.following_count,
            'liked_posts': [post.id for post in self.liked_posts.all()]
        }

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=16, blank=False)
    post = models.TextField()
    likes = models.IntegerField(default=0)
    liked_users = models.ManyToManyField(User, verbose_name='Liked Users', related_name='users_liked', blank=True)
    date = models.DateTimeField(auto_now_add=True)

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
            'date': self.date.strftime('%Y-%m-%d'),
        }

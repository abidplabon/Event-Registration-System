import win32timezone
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    image = models.ImageField(upload_to="post_images")
    event_title = models.CharField(max_length=264, blank=True)
    date = models.DateTimeField()
    time = models.TimeField()
    location = models.CharField(max_length=264, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)  # New field for storing the number of likes
    max_likes = models.IntegerField(default=1)

    class Meta:
        ordering = ['-upload_date']  # last post will be displayed first


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # to show in database and admin panel
        return '{}  : {}'.format(self.user, self.post)

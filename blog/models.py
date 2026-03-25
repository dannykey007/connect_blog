from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import re


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='post_pics', blank=True, null=True)
    video = models.FileField(upload_to='post_videos', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)
    video_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_total_likes(self):
        return self.likes.count()

   
    @property
    def embed_video_url(self):
        if self.video_url:
            # This regex identifies the 11-character YouTube ID
            regex = r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=|shorts\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
            match = re.search(regex, self.video_url)
            if match:
                video_id = match.group(1)
                # Returns the specific 'embed' format YouTube requires to play on other sites
                return f"https://www.youtube.com/embed/{video_id}"
        return self.video_url


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    is_hidden = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        User, related_name='comment_likes', blank=True)

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    user_id = models.IntegerField(blank=True, null=True)  # Default user_id as per requirement

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return self.name
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Post(models.Model):
    title: models.CharField = models.CharField(max_length=120)
    content: models.TextField = models.TextField()
    author: models.ForeignKey[User] = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return str(self.title)


class Comment(models.Model):
    text: models.TextField = models.TextField()
    author: models.ForeignKey[User] = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return str(self.text)

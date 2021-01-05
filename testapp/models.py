from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class TestModel(models.Model):
    title = models.CharField(max_length=255)


class TestModelWithUserField(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TestModelWithAuthorField(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

from django.db import models


class Lesson(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    teachers = models.ManyToManyField('')
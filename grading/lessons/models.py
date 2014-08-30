from django.db import models
from django.contrib.auth.models import User
from usermanage.models import SchoolClass


class Question(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%r' % (self.title)


class Lesson(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    school_class = models.ForeignKey(SchoolClass)
    questions = models.ManyToManyField(Question)

    def __unicode__(self):
        return u'%r' % (self.name)

    def get_absolute_url(self):
        return '/lesson/%i/' % (self.id)

    def get_edit_url(self):
        return '/lesson/edit-%i/' % (self.id)


class Response(models.Model):
    text = models.TextField(blank=True, null=True)
    answerer = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    comment = models.TextField(blank=True, null=True)
    seen = models.BooleanField(default=False)
    lesson = models.ForeignKey(Lesson)

    def __unicode__(self):
        return u'%r' % (self.question.title)

from django.db import models
from django.contrib.auth.models import User


class SchoolClass(models.Model):
    name = models.CharField(max_length=255)
    teachers = models.ManyToManyField(User, related_name='teachers')
    students = models.ManyToManyField(User, related_name='students')

    def __unicode__(self):
        return u'<SchoolClass: %r>' % (self.name)

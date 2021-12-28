from django.db import models


class Course(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    teachers = models.ManyToManyField('auth.User', related_name='teacher')
    students = models.ManyToManyField('auth.User', related_name='student')

    class Meta:
        ordering = ['created']

from django.db import models


class Homework(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='homeworks', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', related_name='homeworks', on_delete=models.CASCADE)
    lecture = models.ForeignKey('Lecture', related_name='homeworks', on_delete=models.CASCADE)
    hometask = models.ForeignKey('Hometask', related_name='homeworks', on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    grade = models.IntegerField(null=True, default=None)

    class Meta:
        ordering = ['created']

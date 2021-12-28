from django.db import models


class Lecture(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='lectures', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/')
    course = models.ForeignKey('Course', related_name='lectures', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

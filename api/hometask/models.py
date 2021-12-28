from django.db import models


class Hometask(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='hometasks', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', related_name='hometasks', on_delete=models.CASCADE)
    lecture = models.ForeignKey('Lecture', related_name='hometasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=False)

    class Meta:
        ordering = ['created']

from django.db import models


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', related_name='comments', on_delete=models.CASCADE)
    lecture = models.ForeignKey('Lecture', related_name='comments', on_delete=models.CASCADE)
    hometask = models.ForeignKey('Hometask', related_name='comments', on_delete=models.CASCADE)
    homework = models.ForeignKey('Homework', related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(blank=False)

    class Meta:
        ordering = ['created']

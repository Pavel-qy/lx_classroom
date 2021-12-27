from django.db import models


class Course(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    teachers = models.ManyToManyField('auth.User', related_name='teacher')
    students = models.ManyToManyField('auth.User', related_name='student')

    class Meta:
        ordering = ['created']


class Lecture(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='lectures', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/')
    course = models.ForeignKey('Course', related_name='lectures', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']


class Hometask(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='hometasks', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', related_name='hometasks', on_delete=models.CASCADE)
    lecture = models.ForeignKey('Lecture', related_name='hometasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=False)

    class Meta:
        ordering = ['created']


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

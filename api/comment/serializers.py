from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    course = serializers.ReadOnlyField(source='course.id')
    lecture = serializers.ReadOnlyField(source='lecture.id')
    hometask = serializers.ReadOnlyField(source='hometask.id')

    class Meta:
        model = Comment
        fields = ['id', 'created', 'owner', 'course', 'lecture', 'hometask', 'homework', 'body']

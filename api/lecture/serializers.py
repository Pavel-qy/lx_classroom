from rest_framework import serializers
from .models import Lecture


class LectureSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    hometasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Lecture
        fields = ['id', 'created', 'owner', 'course', 'title', 'document', 'hometasks']

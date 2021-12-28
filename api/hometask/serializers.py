from rest_framework import serializers
from .models import Hometask


class HometaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    course = serializers.ReadOnlyField(source='course.id')
    homeworks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Hometask
        fields = ['id', 'created', 'owner', 'course', 'lecture', 'title', 'body', 'homeworks']

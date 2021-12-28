from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    lectures = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    hometasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    homeworks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'created', 'owner', 'title', 'teachers', 'students',
            'lectures', 'hometasks', 'homeworks', 'comments'
        ]

    def validate(self, attrs):
        if set(attrs['teachers']) & set(attrs['students']):
            raise serializers.ValidationError(
                {'teachers_students': "Fields 'Teachers' and 'Students' cannot include the same users."}
            )
        return attrs

from rest_framework import serializers
from .models import Course
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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
    
    def create(self, validated_data):
        channel_layer = get_channel_layer()
        students_list = [student.id for student in validated_data['students']]
        teachers_list = [teacher.id for teacher in validated_data['teachers']]
        course_title = validated_data['title']

        # send message to users that he is enrolled in the course
        for group in students_list:
            async_to_sync(channel_layer.group_send)(
                str(group),  # group name
                {
                    'type': 'notify',  # custom function written in the consumers.py
                    'message': f'Congratulations! You are enrolled in the "{course_title}" course!'
                }
            )
        
        # send message to teachers
        for group in teachers_list:
            async_to_sync(channel_layer.group_send)(
                str(group),
                {
                    'type': 'notify',
                    'message': f'You has been assigned as a teacher for the "{course_title}" course!'
                }
            )
            
        return super().create(validated_data)

    def validate(self, attrs):
        if set(attrs['teachers']) & set(attrs['students']):
            raise serializers.ValidationError(
                {'teachers_students': "Fields 'Teachers' and 'Students' cannot include the same users."}
            )
        return attrs

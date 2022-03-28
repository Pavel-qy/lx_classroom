from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
# from ..tasks import write_some_message_task, write_some_message_task_prior
from .. tasks import WriteSomeMessageTask, WriteSomeMessageTaskPrior



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password fields didn\'t match.'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        # calling tasks without specifying a queue and priority
        # write_some_message_task.apply_async(("Registered user data", validated_data))
        # write_some_message_task_prior.apply_async(("Registered user data", validated_data), countdown=3)
        
        # calling tasks with specifying a queue and priority      
        # write_some_message_task.apply_async(("Registered user data", validated_data), queue='users_registration', priority=9)
        # write_some_message_task_prior.apply_async(("Registered user data", validated_data), queue='users_registration', priority=0)
        
        # calling class-based tasks
        WriteSomeMessageTask.apply_async(("Registered user data", validated_data))
        WriteSomeMessageTaskPrior.apply_async(("Registered user data", validated_data))
        return User

from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    assigned_admin_name = serializers.SerializerMethodField()


    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_by']

    def get_assigned_admin_name(self, obj):
        if obj.assigned_to and obj.assigned_to.assigned_admin:
            return obj.assigned_to.assigned_admin.username
        return None
    

class TaskReportSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    assigned_admin_name = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'status',
             'completion_report', 'worked_hours',
            'assigned_to_username', 'created_by_name', 'assigned_admin_name',
            'created_by'
        ]

    def get_assigned_admin_name(self, obj):
        print("DEBUG: assigned_to =", obj.assigned_to)
        print("DEBUG: assigned_admin =", getattr(obj.assigned_to, 'assigned_admin', None))
        if obj.assigned_to and obj.assigned_to.assigned_admin:
            return obj.assigned_to.assigned_admin.username
        return None



from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    assigned_admin_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'assigned_admin', 'assigned_admin_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'assigned_admin': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def get_assigned_admin_name(self, obj):
        if obj.assigned_admin:
            return obj.assigned_admin.username  
        return None

from rest_framework import serializers
from .models import *

class ProjectSerializer(serializers.ModelSerializer):

    project_platform = serializers.SerializerMethodField()
    project_stack = serializers.SerializerMethodField()
    project_genre = serializers.SerializerMethodField()
    project_university = serializers.SerializerMethodField()
    # collaborator = serializers.SerializerMethodField()

    def get_project_platform(self, instance):
        platforms = instance.project_platform.all()
        return [platform.platform_name for platform in platforms]
    
    def get_project_stack(self, instance):
        stacks = instance.project_stack.all()
        return [stack.stack_name for stack in stacks]
    
    def get_project_genre(self, instance):
        genres = instance.project_genre.all()
        return [genre.genre_name for genre in genres]
    
    def get_project_university(self, instance):
        universities = instance.project_university.all()
        return [university.university_name for university in universities]
    
    class Meta:
        model = Project
        exclude = ('scrap_accounts', 'like_accounts')
        read_only_fields = ('id', 'period', 'scrap_accounts', 'like_accounts', 'like_count', 'view_count')
        
        
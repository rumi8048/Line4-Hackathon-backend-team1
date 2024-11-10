from rest_framework import serializers
from .models import *

class CollaboratorMiddleTableSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField()
    class Meta:
        model = CollaboratorMiddleTable
        fields = ['account', 'role', 'is_leader']

    # 유저 이름을 출력하도록 변경
    def get_account(self, instance):
        return instance.account.user.username
        
class ProjectSerializer(serializers.ModelSerializer):
    project_platform = serializers.SerializerMethodField()
    project_stack = serializers.SerializerMethodField()
    project_genre = serializers.SerializerMethodField()
    project_university = serializers.SerializerMethodField()
    collaborator = CollaboratorMiddleTableSerializer(source='collaboratormiddletable_set', many=True)
    upload_date = serializers.SerializerMethodField()

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

    def get_collaborator(self, instance):
        collaborators = instance.collaborator.all()
        return [collaborator.user.username for collaborator in collaborators]
    
    def get_upload_date(self, instance):
        return instance.upload_date.strftime('%Y-%m-%d')
    
    class Meta:
        model = Project
        exclude = ('scrap_accounts', 'like_accounts')
        read_only_fields = ('id', 'period', 'scrap_accounts', 'like_accounts', 'like_count', 'view_count')
        
    
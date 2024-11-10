from django.forms import ValidationError
from rest_framework import serializers

from accounts.models import Account
from ptn_project.models import CollaboratorMiddleTable, Project
from search.models import GenreTag, Platform, StackTag, UniversityTag
from .models import *

class CollaboratorMiddleTableSerializer(serializers.ModelSerializer):
    account_id = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())  # account 필드를 쓰기 가능하게 설정
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = CollaboratorMiddleTable
        fields = ['role', 'is_leader', 'account_id', 'nickname']
        
    # 유저 이름을 출력하도록 변경
    def get_nickname(self, instance):
        return instance.account.nickname

class ProjectImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProjectImage
        fields = ['image']

class ProjectSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    collaborator = CollaboratorMiddleTableSerializer(source='collaboratormiddletable_set', many=True)
    upload_date = serializers.SerializerMethodField()
    project_platform = serializers.SlugRelatedField(
        slug_field='platform_name',
        queryset=Platform.objects.all(),
        many=True
    )
    project_stack = serializers.SlugRelatedField(
        slug_field='stack_name',
        queryset=StackTag.objects.all(),
        many=True
    )
    project_genre = serializers.SlugRelatedField(
        slug_field='genre_name',
        queryset=GenreTag.objects.all(),
        many=True
    )
    project_university = serializers.SlugRelatedField(
        slug_field='university_name',
        queryset=UniversityTag.objects.all(),
        many=True
    )
    

    class Meta:
        model = Project
        exclude = ['scrap_accounts', 'like_accounts']
        read_only_fields = ('id', 'scrap_accounts', 'like_accounts', 'like_count')
    
    def get_images(self, instance):
        # request 객체를 통해 base URL 가져오기
        request = self.context.get('request')
        if request:
            return [
                request.build_absolute_uri(image.image.url)
                for image in instance.project_image.all()
            ]
        else:
            # request 객체가 없을 경우 상대 경로만 반환
            return [image.image.url for image in instance.project_image.all()]
    
    def get_upload_date(self, instance):
        return instance.upload_date.strftime('%Y-%m-%d')
    
    
    def create(self, validated_data):
        # ManyToMany 필드 데이터 분리
        platforms_data = validated_data.pop('project_platform', [])
        genres_data = validated_data.pop('project_genre', [])
        stacks_data = validated_data.pop('project_stack', [])
        universities_data = validated_data.pop('project_university', [])
        collaborators_data = validated_data.pop('collaboratormiddletable_set', [])

         # Project 객체 생성
        project = Project.objects.create(**validated_data)

        # ManyToMany 필드 설정
        project.project_platform.set(platforms_data)
        project.project_genre.set(genres_data)
        project.project_stack.set(stacks_data)
        project.project_university.set(universities_data)

        # Collaborator 처리
        for collaborator_data in collaborators_data:
            account = collaborator_data.get('account_id')
            role = collaborator_data.get('role')
            is_leader = collaborator_data.get('is_leader')
            CollaboratorMiddleTable.objects.create(
                project=project, account=account,
                role=role, is_leader= is_leader
            )

        # 다중 이미지 처리
        image_set = self.context['request'].FILES
        print(image_set)
        for image_data in image_set.getlist('image'):
            ProjectImage.objects.create(project=project, image=image_data)
        return project
    def update(self, instance, validated_data):
        # ManyToMany 필드 데이터 분리
        platforms_data = validated_data.pop('project_platform', [])
        genres_data = validated_data.pop('project_genre', [])
        stacks_data = validated_data.pop('project_stack', [])
        universities_data = validated_data.pop('project_university', [])
        collaborators_data = validated_data.pop('collaboratormiddletable_set', [])

        # 기존 이미지를 삭제
        existing_images = ProjectImage.objects.filter(project=instance)
        for image in existing_images:
            # 실제 파일 시스템에서 이미지 파일 삭제
            image.image.delete(save=False)
            image.delete()

        # 기본 Project 객체 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()


        # ManyToMany 필드 설정
        instance.project_platform.set(platforms_data)
        instance.project_genre.set(genres_data)
        instance.project_stack.set(stacks_data)
        instance.project_university.set(universities_data)

         # 기존 CollaboratorMiddleTable 항목 삭제
        instance.collaboratormiddletable_set.all().delete()
        
        # Collaborator 처리
        for collaborator_data in collaborators_data:
            account = collaborator_data.get('account_id')
            role = collaborator_data.get('role')
            is_leader = collaborator_data.get('is_leader')
            CollaboratorMiddleTable.objects.create(
                project=instance, account=account,
                role=role, is_leader= is_leader
            )

        # 다중 이미지 처리
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            ProjectImage.objects.create(project=instance, image=image_data)
        return instance
    
class AccountSerializer(serializers.ModelSerializer):
    university = serializers.SerializerMethodField()
    
    def get_university(self, instance):
        return instance.user_university.university_name
    class Meta:
        model = Account
        fields = ['id', 'nickname', 'university']
        read_only_fields = ('id', 'nickname', 'university')
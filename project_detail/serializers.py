from rest_framework import serializers
from accounts.models import Account
from ptn_project.models import CollaboratorMiddleTable, Comment, Discussion, DiscussionImage, InComment, Project
from ptn_project.serializers import CollaboratorMiddleTableSerializer
from .models import *


class InCommentSerializer(serializers.ModelSerializer):
    upload_date = serializers.SerializerMethodField()
    in_comment_writer = serializers.SerializerMethodField()
    class Meta:
        model = InComment
        fields = ['id','in_comment_writer', 'in_comment', 'upload_date']
        read_only_fields = ['id','in_comment_writer', 'parent_comment', 'upload_date']
    
    def get_in_comment_writer(self, instance):
        return instance.in_comment_writer.nickname
    
    def get_upload_date(self, instance):
        return instance.upload_date.strftime('%Y-%m-%d')
        

class CommentSerializer(serializers.ModelSerializer):
    in_comment = InCommentSerializer(many=True, read_only=True)  # 대댓글 추가
    upload_date = serializers.SerializerMethodField()
    comment_writer = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'in_comment', 'comment_writer', 'upload_date']
        read_only_fields = ['id', 'in_comment', 'comment_writer', 'upload_date']

    def get_comment_writer(self, instance):
        return instance.comment_writer.nickname
    
    def get_upload_date(self, instance):
        return instance.upload_date.strftime('%Y-%m-%d')

class DiscussionImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = DiscussionImage
        fields = ['image']

class DiscussionSerializer(serializers.ModelSerializer):
    discussion_writer = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Discussion
        fields = ['id', 'discussion_writer', 'title', 'description', 'images']
        read_only_fields = ['id']
        
    def get_discussion_writer(self, instance):
        # 프로젝트와 계정이 일치하는 CollaboratorMiddleTable의 정보를 가져옴
        collaborator = CollaboratorMiddleTable.objects.filter(
            project=instance.project,
            account=instance.discussion_writer
        ).first()
        if collaborator:
            return {
                'nickname': collaborator.account.nickname,
                'role': collaborator.role,
                'university': collaborator.account.user_university.university_name,
            }
        return None
    
    def get_discussion_image(self, instance):
        # request 객체를 통해 base URL 가져오기
        request = self.context.get('request')
        if request:
            return [
                request.build_absolute_uri(image.image.url)
                for image in instance.discussion_image.all()
            ]
        else:
            # request 객체가 없을 경우 상대 경로만 반환
            return [image.image.url for image in instance.discussion_image.all()]
        
    
    def get_images(self, instance):
        # request 객체를 통해 base URL 가져오기
        request = self.context.get('request')
        if request:
            return [
                request.build_absolute_uri(image.image.url)
                for image in instance.discussion_image.all()
            ]
        else:
            # request 객체가 없을 경우 상대 경로만 반환
            return [image.image.url for image in instance.discussion_image.all()]
        
    def create(self, validated_data):
        discussion = Discussion.objects.create(**validated_data)
        # 다중 이미지 처리
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            DiscussionImage.objects.create(discussion=discussion, image=image_data)
        return discussion
    
    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.title = validated_data.get('title', instance.title)
        if 'description' in validated_data:
            instance.description = validated_data.get('description', instance.description)
        instance.save()

        image_set = self.context['request'].FILES
        if (image_set):
            # 기존 이미지를 삭제하고 실제 파일 시스템에서도 삭제
            existing_images = DiscussionImage.objects.filter(discussion=instance)
            for image in existing_images:
                image.image.delete(save=False)  # 실제 파일 시스템에서 이미지 파일 삭제
                image.delete()

        # 다중 이미지 처리
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            DiscussionImage.objects.create(discussion=instance, image=image_data)

        return instance
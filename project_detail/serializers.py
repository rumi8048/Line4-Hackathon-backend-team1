from rest_framework import serializers
from accounts.models import Account
from ptn_project.models import AIFeedbackSummary, CollaboratorMiddleTable, Comment, Discussion, DiscussionImage, FeedbackImage, InComment, Project, UserFeedback
from .models import *
from django.utils import timezone
BASE_URL = 'https://dgu-booth.shop'

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        base_url = BASE_URL
        representation['image'] = base_url + instance.image.url
        return representation
    
class DiscussionSerializer(serializers.ModelSerializer):
    discussion_writer = serializers.SerializerMethodField()
    images = DiscussionImageSerializer(source='discussion_image', many=True, required=False)

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


class FeedbackImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = FeedbackImage
        fields = ['image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        base_url = BASE_URL
        representation['image'] = base_url + instance.image.url
        return representation
    
class FeedbackSerializer(serializers.ModelSerializer):
    feedback_writer = serializers.SerializerMethodField()
    upload_date = serializers.SerializerMethodField()
    images = FeedbackImageSerializer(source='feedback_image', many=True, required=False)
    # PrimaryKeyRelatedField로 설정하여 id 값만 받을 수 있도록 합니다
    discussion = serializers.PrimaryKeyRelatedField(queryset=Discussion.objects.all(), many=True, required=False) 
    class Meta:
        model = UserFeedback
        fields = ['id', 'feedback_writer', 'is_adopted', 'feedback_description', 'images' ,'discussion', 'upload_date']
        read_only_fields = ['id', 'is_adopted']
    

    def get_upload_date(self, instance):
        return instance.upload_date.strftime('%Y-%m-%d')
    
    def get_feedback_writer(self, instance):
       return instance.feedback_writer.nickname
        
    def create(self, validated_data):
        discussions = validated_data.pop('discussion', [])
        
        feedback = UserFeedback.objects.create(**validated_data)
        feedback.discussion.set(discussions)
        
        # 다중 이미지 처리
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            FeedbackImage.objects.create(feedback=feedback, image=image_data)
        return feedback
    
    def update(self, instance, validated_data):

        discussions = validated_data.pop('discussion', [])
        if 'feedback_description' in validated_data:
            instance.feedback_description = validated_data.get('feedback_description', instance.feedback_description)
        instance.save()

        if discussions:
            instance.discussion.set(discussions)
    
        image_set = self.context['request'].FILES
        if (image_set):
            # 기존 이미지를 삭제하고 실제 파일 시스템에서도 삭제
            existing_images = FeedbackImage.objects.filter(feedback=instance)
            for image in existing_images:
                image.image.delete(save=False)  # 실제 파일 시스템에서 이미지 파일 삭제
                image.delete()

        # 다중 이미지 처리
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            FeedbackImage.objects.create(feedback=instance, image=image_data)

        return instance
class FeedbackListSerializer(serializers.ModelSerializer):
    feedback_writer = serializers.SerializerMethodField()
    upload_date = serializers.SerializerMethodField()
    images = FeedbackImageSerializer(source='feedback_image', many=True, required=False)
    discussion = DiscussionSerializer(many=True, read_only=True)
    can_update_and_delete = serializers.SerializerMethodField()
    is_collaborator = serializers.SerializerMethodField()

    def get_is_collaborator(self, instance):
        return instance.feedback_writer in instance.project.collaborator.all()
    
    def get_feedback_writer(self, instance):
       return instance.feedback_writer.nickname
    def get_upload_date(self, instance):
        return instance.upload_date.strftime('%Y-%m-%d')
    def get_can_update_and_delete(self, instance):
        return instance.feedback_writer == self.context['request'].user.account or self.context['request'].user.is_superuser
    
    class Meta:
        model = UserFeedback
        exclude = ['project']
        read_only_fields = ['id', 'is_adopted']


class AiSummarySerializer(serializers.ModelSerializer):
    upload_date = serializers.SerializerMethodField()
    class Meta:
        model = AIFeedbackSummary
        fields = ['id', 'upload_date', 'title', 'feedback_summary']
        read_only_fields = ['id', 'upload_date']
    
    def get_upload_date(self, instance):
        return instance.upload_date.strftime('%Y-%m-%d')
    
    # def create(self, validated_data):
    #     upload_date = timezone.now()
    #     base_title = f"{upload_date.strftime('%y년 %m월 %d일')} 보고서"
    #     title = base_title
    #     counter = 1

    #     # 동일한 이름이 있을 경우 숫자를 늘려가면서 title 설정
    #     while AIFeedbackSummary.objects.filter(title=title).exists():
    #         title = f"{base_title} ({counter})"
    #         counter += 1

    #     validated_data['title'] = title
    #     return super().create(validated_data)
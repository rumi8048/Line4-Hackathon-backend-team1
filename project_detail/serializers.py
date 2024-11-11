from rest_framework import serializers
from ptn_project.models import Comment, InComment, Project
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
    
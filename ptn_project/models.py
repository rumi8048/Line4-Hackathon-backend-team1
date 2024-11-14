from django.db import models
from accounts.models import Account
from search.models import GenreTag, UniversityTag, StackTag, Platform

def thumbnail_upload_path(instance, filename):
    return f'ptn_project/thumbnail/{instance.id}/{filename}'

def detail_image_upload_path(instance, filename):
    return f'ptn_project/detail_image/{instance.id}/{filename}'

def feedback_image_upload_path(instance, filename):
    return f'ptn_project/feedback_image/{instance.id}/{filename}'

def discussion_image_upload_path(instance, filename):
    return f'ptn_project/discussion_image/{instance.id}/{filename}'

# Create your models here.

class Project(models.Model):
    project_name = models.CharField(null=False, max_length=255)
    project_thumbnail = models.ImageField(null=True, upload_to=thumbnail_upload_path, default='default.png')
    # 간단한 설명
    simple_description = models.TextField(null=False, default="")
    # 세부 설명
    detail_description = models.TextField(null=False, default="")
    # 업로드 날짜
    upload_date = models.DateTimeField(auto_now_add=True)
    # 수행 기간
    period = models.TextField(null=False, default="")

    # 웹, ios, 안드로이드 링크
    web_link = models.TextField(null=True,blank=True, default="")
    ios_link = models.TextField(null=True,blank=True, default="")
    android_link = models.TextField(null=True,blank=True, default="")

    # 스크랩한 유저 계정을 저장하는 필드
    scrap_accounts = models.ManyToManyField(Account, related_name= "scrap_projects")
    # 좋아요 누른 유저 계정을 확인하는 MTM 필드
    like_accounts = models.ManyToManyField(Account, related_name= "like_projects")
    like_count = models.IntegerField(null=False, default=0)
    
    # 플랫폼
    project_platform = models.ManyToManyField(Platform, related_name= "project")
    # 장르
    project_genre = models.ManyToManyField(GenreTag, related_name= "project")
    # 스택
    project_stack = models.ManyToManyField(StackTag, related_name= "project")
    # 대학
    project_university = models.ManyToManyField(UniversityTag, related_name= "project")
    # 참여자
    collaborator = models.ManyToManyField(Account, through='CollaboratorMiddleTable', related_name='collaborator_projects')

    

class CollaboratorMiddleTable(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    # 사용자 역할
    role = models.CharField(null=False, max_length=255)
    # 프로젝트 대표 여부
    is_leader = models.BooleanField(default=False, null=False)

class ProjectImage(models.Model):
    # 프로젝트를 외래키로 가짐
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_image')
    image = models.ImageField(null=True, upload_to=detail_image_upload_path)



# AI 가 요약해준 피드백을 저장하는 모델
class AIFeedbackSummary(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ai_feedback_summary')
    title = models.CharField(null=False, max_length=255)
    feedback_summary = models.JSONField(null=False, blank=True, default=dict)
    # 업로드 날짜
    upload_date = models.DateTimeField(auto_now_add=True)

# 고민 되었던 부분 모델
class Discussion(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='discussion')
    discussion_writer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='discussion')
    title = models.CharField(null=False, max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=False, default="")


# 사용자들이 작성한 피드백을 저장하는 모델
class UserFeedback(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='feedback')
    feedback_writer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='feedback')
    # 업로드 날짜
    upload_date = models.DateTimeField(auto_now_add=True)
    # 피드백 채택 여부 확인
    is_adopted = models.BooleanField(default=False, null=False)
    # 피드백 내용
    feedback_description = models.TextField(null=False, default="")
    discussion = models.ManyToManyField(Discussion, related_name='feedback')

class FeedbackImage(models.Model):
    # 피드백을 외래키로 가짐
    feedback = models.ForeignKey(UserFeedback, on_delete=models.CASCADE, related_name='feedback_image')
    image = models.ImageField(null=True, upload_to=feedback_image_upload_path)

class DiscussionImage(models.Model):
    # 고민 되었던 부분을 외래키로 가짐
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='discussion_image')
    image = models.ImageField(null=True, upload_to=discussion_image_upload_path)

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comment')
    comment_writer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='comment')
    upload_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=False, default="")

# 대댓글 모델
class InComment(models.Model):
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='in_comment')
    in_comment_writer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='in_comment')
    upload_date = models.DateTimeField(auto_now_add=True)
    in_comment = models.TextField(null=False, default="")
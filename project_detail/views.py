from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from project_detail.ai_script import generate_report
from ptn_project.models import Comment, Project
from ptn_project.serializers import ProjectSerializer
from .models import *
from .serializers import *
from .permissions import IsCommentOwnerOrReadOnly, IsDiscussionOwnerOrReadOnly, IsFeedbackOwnerOrReadOnly, IsInCommentOwnerOrReadOnly, IsPossibleCommentsOrReadOnly, IsPossibleDiscussionOrReadOnly, IsProjectOwnerOrReadOnly
# Create your views here.
class ProjectDetailViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Project.objects.all()

    def get_permissions(self):
        if self.action in ["update", "create", "destroy", "partial_update"]:
            return [IsProjectOwnerOrReadOnly()]
        return []
    
    def get_serializer_class(self):
        return ProjectSerializer  

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': '프로젝트가 성공적으로 삭제되었습니다.'})
    

    @action(methods=['GET'], detail=True, url_path="like")
    def like(self, request, pk=None):
        project = self.get_queryset().filter(id=pk).first()
        if request.user.account in project.like_accounts.all():
            project.like_accounts.remove(request.user.account)  # 이미 좋아요 누른 경우, 취소
            project.like_count -= 1
            project.save()
        else:
            project.like_accounts.add(request.user.account)  # 좋아요 추가
            project.like_count += 1
            project.save()
        serializer = ProjectSerializer(project, context={'request': request})
        return Response(serializer.data)
    
    @action(methods=['GET'], detail=True, url_path="scrap")
    def scrap(self, request, pk=None):
        project = self.get_queryset().filter(id=pk).first()
        if request.user.account in project.scrap_accounts.all():
            project.scrap_accounts.remove(request.user.account)  # 이미 좋아요 누른 경우, 취소
            project.save()
            return Response({'message': '스크랩이 취소되었습니다'})
        else:
            project.scrap_accounts.add(request.user.account)  # 좋아요 추가
            project.save()
            return Response({'message': '스크랩 되었습니다'})
    
# 댓글 디테일 조회 수정 삭제
class DetailCommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            return [IsCommentOwnerOrReadOnly()]
        return []
    def destroy (self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': '댓글이 성공적으로 삭제되었습니다.'})
    
# 게시물에 있는 댓글 목록 조회, 게시물에 댓글 작성
class CommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsPossibleCommentsOrReadOnly()]
        return []
    
    def get_queryset(self):
        project = self.kwargs.get("project_id")
        queryset = Comment.objects.filter(project_id=project)
        return queryset
    
    def create(self, request, project_id=None):
        project = get_object_or_404(Project, id=project_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project, comment_writer=request.user.account)
        return Response(serializer.data)
    
class InCommentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = InCommentSerializer
    
    def get_permissions(self):
        if self.action in ["create"]:
            return [IsPossibleCommentsOrReadOnly()]
        return []

    def get_queryset(self):
        # URL에서 comment_id를 가져와 해당하는 대댓글 리스트를 필터링
        comment_id = self.kwargs.get("comment_id")
        return InComment.objects.filter(parent_comment_id=comment_id)

    def create(self, request, project_id=None, comment_id=None):
        # URL에서 comment_id에 해당하는 Comment 객체를 가져옴
        parent_comment = get_object_or_404(Comment, id=comment_id)
        
        # 요청 데이터에 parent_comment를 포함하여 대댓글을 생성
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(parent_comment=parent_comment, in_comment_writer=request.user.account)
        
        return Response(serializer.data)
    
class DetailInCommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = InComment.objects.all()
    serializer_class = InCommentSerializer
    
    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            return [IsInCommentOwnerOrReadOnly()]
        return []
    
    def destroy (self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': '대댓글이 성공적으로 삭제되었습니다.'})
    
class DiscussionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    
    def create(self, request, project_id=None):
        project = get_object_or_404(Project, id=project_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(discussion_writer=request.user.account, project=project)
        return Response(serializer.data)
    
    def get_permissions(self):
        if self.action in ["create"]:
            return [IsPossibleDiscussionOrReadOnly()]
        return []
    
    def get_queryset(self):
        project = self.kwargs.get("project_id")
        queryset = Discussion.objects.filter(project_id=project)
        return queryset

class DetailDiscussionViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    
    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            return [IsDiscussionOwnerOrReadOnly()]
        return []
    
    def destroy (self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': '고민 게시글이 성공적으로 삭제되었습니다.'})

class FeedbackViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = UserFeedback.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return FeedbackSerializer
        return FeedbackListSerializer
    
    def create(self, request, project_id=None):
        project = get_object_or_404(Project, id=project_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(feedback_writer=request.user.account, project=project)
        return Response(serializer.data)
    
    def get_permissions(self):
        if self.action in ["create"]:
            return [IsPossibleDiscussionOrReadOnly()]
        return []
    
    def get_queryset(self):
        project = self.kwargs.get("project_id")
        queryset = UserFeedback.objects.filter(project_id=project)
        return queryset

class DetailFeedbackViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = UserFeedback.objects.all()
    
    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return FeedbackSerializer
        return FeedbackListSerializer
    
    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            return [IsFeedbackOwnerOrReadOnly()]
        return []
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({'message': '피드백이 성공적으로 수정되었습니다.'})

    def destroy (self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': '피드백이 성공적으로 삭제되었습니다.'})
    
    @action(methods=['POST'], detail=True, url_path="adopt")
    def adopt(self, request, project_id=None, pk=None):
        feedback = self.get_queryset().filter(id=pk).first()
        if not feedback:
            return Response({'message': '피드백을 찾을 수 없습니다.'}, status=404)
        
        point = request.data.get('point')
        if point is None:
            return Response({'message': '포인트 값을 입력해주세요.'}, status=400)
        
        try:
            point = int(point)
        except ValueError:
            return Response({'message': '유효한 포인트 값을 입력해주세요.'}, status=400)
        
        feedback.is_adopted = True
        feedback.save()
        
        feedback_writer = feedback.feedback_writer
        feedback_writer.total_point += point
        feedback_writer.save()
        
        return Response({'message': '피드백이 채택되었고 포인트가 추가되었습니다.'})
    
class AiSummaryViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):

    def get_queryset(self):
        return AIFeedbackSummary.objects.all()
    
    def get_serializer_class(self):
        return AiSummarySerializer

    def list(self, request, project_id=None):
        project = Project.objects.filter(id=project_id).first()
        if not project:
            return Response({'message': '프로젝트를 찾을 수 없습니다.'}, status=404)
        
        ai_feedback_summaries = AIFeedbackSummary.objects.filter(project=project)
        serializer = AiSummarySerializer(ai_feedback_summaries, many=True)
        return Response(serializer.data)
    
    def create(self, request, project_id=None):
        project = get_object_or_404(Project, id=project_id)
        user = request.user.account

        # Check if the user has enough points
        if user.total_point <= 0:
            return Response({'message': '포인트가 부족합니다.'})
        
        serializer = FeedbackListSerializer(project.feedback, many=True, context={'request': request})
        summary_output = generate_report(serializer.data)
        
        upload_date = timezone.now()
        base_title = f"{upload_date.strftime('%y년 %m월 %d일')} 보고서"
        title = base_title
        counter = 1

        # 동일한 이름이 있을 경우 숫자를 늘려가면서 title 설정
        while AIFeedbackSummary.objects.filter(title=title).exists():
            title = f"{base_title} ({counter})"
            counter += 1

        result = AIFeedbackSummary.objects.create(project=project, feedback_summary=summary_output, title=title, upload_date=upload_date)
        # Decrease the user's total points by 1
        user.total_point -= 1
        user.save()

        return Response(AiSummarySerializer(result).data)
    
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from ptn_project.models import Comment, Project
from ptn_project.serializers import ProjectSerializer
from .models import *
from .serializers import *
from .permissions import IsCommentOwnerOrReadOnly, IsInCommentOwnerOrReadOnly, IsPossibleCommentsOrReadOnly, IsProjectOwnerOrReadOnly
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
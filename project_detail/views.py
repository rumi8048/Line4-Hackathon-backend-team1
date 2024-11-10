from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from ptn_project.models import Project
from ptn_project.serializers import ProjectSerializer
from .models import *
from .serializers import *
from .permissions import IsProjectOwnerOrReadOnly
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
    
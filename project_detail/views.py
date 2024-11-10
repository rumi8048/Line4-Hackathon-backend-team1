from django.shortcuts import get_object_or_404, render
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
    
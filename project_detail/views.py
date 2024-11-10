from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, mixins

from ptn_project.models import Project
from .models import *
from .serializers import *
# Create your views here.
class ProjectDetailViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve' :
            return ProjectDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return ProjectCreateSerializer
        return ProjectDetailSerializer     

  
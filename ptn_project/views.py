from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import *
from .serializers import *
# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    
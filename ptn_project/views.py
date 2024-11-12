from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from django.contrib.auth.models import User
from ptn_project.models import Project
from .models import *
from .serializers import *
# Create your views here.
class ProjectViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = Project.objects.all()
    
    def get_serializer_class(self):
        return ProjectSerializer    

    def create(self, request):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
         # project_thumbnail이 null인 경우 기본 이미지 설정
        if not serializers.validated_data.get('project_thumbnail'):
            serializers.validated_data['project_thumbnail'] = 'ptn_project/default_image.png'

        self.perform_create(serializers)
        return Response({'message': '프로젝트가 성공적으로 생성되었습니다.', 'project_id': serializers.data.get('id')})

    def list(self, request):
        project = self.get_queryset().order_by('?')
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path="recommend")
    def recommend(self, request):
        user = request.user.account  # 현재 요청한 사용자의 Account 모델 가져오기
        
        favorite_genres = user.favorite_genre.all()  # 사용자의 favorite_genre 필드
        # 사용자의 favorite_genre 태그를 포함하는 프로젝트 필터링
        projects = Project.objects.filter(project_genre__in=favorite_genres).distinct()
        
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='filter')
    def filter_by_genre(self, request):
        genres = request.data.get('genre', [])
        if not genres:
            return Response({'error': 'No genres provided.'})

        genre_tags = GenreTag.objects.filter(genre_name__in=genres)
        if not genre_tags.exists():
            return Response({'error': 'No matching genres found.'})

        # 모든 장르 태그가 포함된 프로젝트 필터링
        projects = Project.objects.all()
        for genre_tag in genre_tags:
            projects = projects.filter(project_genre=genre_tag)

        projects = projects.distinct()
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)
      


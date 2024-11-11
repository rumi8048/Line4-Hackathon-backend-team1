from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from search.serialiers import *
from .models import *

# 장르 목록을 출력하는 viewset
class GenreViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
        
    def get_queryset(self):
        return GenreTag.objects.all()
    
    def get_serializer_class(self):
        return GenreTagSerializer

    def list(self, request, *args, **kwargs):
        # 기존의 list 메서드를 호출하여 data를 가져옴
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # 각 객체의 genre_name만 추출하여 리스트로 변환
        genre_list = [genre["genre_name"] for genre in serializer.data]
        # data를 배열 형태로 감싸서 반환
        return Response({"genre": genre_list})
    
    @action(detail=False, methods=['post'], url_path='input')
    def filter_by_genre(self, request):
        genres = request.data.get('genre_name', [])
        if not genres:
            return Response({'error': 'No genres provided.'})

         # 입력된 stack_name이 영어인지 한글인지 확인
        if genres.isalpha() and genres[0].lower() in 'abcdefghijklmnopqrstuvwxyz':
            # 영어일 경우 입력된 길이만큼 대소문자 구분 없이 검색
            genre_tags = GenreTag.objects.filter(genre_name__istartswith=genres)
        else:
            # 한글일 경우 입력된 길이만큼 앞부분이 일치하는 데이터 검색
            genre_tags = GenreTag.objects.filter(genre_name__startswith=genres)

        if not genre_tags.exists():
            return Response({'error': 'No matching stacks found.'})

        # 데이터를 직렬화하고, 배열 형태로 반환
        serializer = self.get_serializer(genre_tags, many=True)
        genre_list = [genre["genre_name"] for genre in serializer.data]
        return Response({"genre": genre_list})
    
# 스택 목록을 출력하는 viewset
class StackViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
        
    def get_queryset(self):
        return StackTag.objects.all()
    
    def get_serializer_class(self):
        return StackTagSerializer

    def list(self, request, *args, **kwargs):
        # 기존의 list 메서드를 호출하여 data를 가져옴
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # 각 객체의 genre_name만 추출하여 리스트로 변환
        stack_list = [stack["stack_name"] for stack in serializer.data]
        # data를 배열 형태로 감싸서 반환
        return Response({"stack": stack_list})
    
    @action(detail=False, methods=['post'], url_path='input')
    def filter_by_stack(self, request):
        stacks = request.data.get('stack_name', [])
        if not stacks:
            return Response({'error': 'No stacks provided.'})

         # 입력된 stack_name이 영어인지 한글인지 확인
        if stacks.isalpha() and stacks[0].lower() in 'abcdefghijklmnopqrstuvwxyz':
            # 영어일 경우 입력된 길이만큼 대소문자 구분 없이 검색
            stack_tags = StackTag.objects.filter(stack_name__istartswith=stacks)
        else:
            # 한글일 경우 입력된 길이만큼 앞부분이 일치하는 데이터 검색
            stack_tags = StackTag.objects.filter(stack_name__startswith=stacks)

        if not stack_tags.exists():
            return Response({'error': 'No matching stacks found.'})

        # 데이터를 직렬화하고, 배열 형태로 반환
        serializer = self.get_serializer(stack_tags, many=True)
        stack_list = [stack["stack_name"] for stack in serializer.data]
        return Response({"stack": stack_list})
    
# 대학 목록을 출력하는 viewset
class UniversityViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
        
    def get_queryset(self):
        return UniversityTag.objects.all()
    
    def get_serializer_class(self):
        return UniversityTagSerializer

    def list(self, request, *args, **kwargs):
        # 기존의 list 메서드를 호출하여 data를 가져옴
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # 각 객체의 genre_name만 추출하여 리스트로 변환
        university_list = [university["university_name"] for university in serializer.data]
        # data를 배열 형태로 감싸서 반환
        return Response({"university": university_list})

    @action(detail=False, methods=['post'], url_path='input')
    def filter_by_university(self, request):
        universities = request.data.get('university_name', [])
        if not universities:
            return Response({'error': 'No genres provided.'})

         # 입력된 stack_name이 영어인지 한글인지 확인
        if universities.isalpha() and universities[0].lower() in 'abcdefghijklmnopqrstuvwxyz':
            # 영어일 경우 입력된 길이만큼 대소문자 구분 없이 검색
            university_tag = UniversityTag.objects.filter(genre_name__istartswith=universities)
        else:
            # 한글일 경우 입력된 길이만큼 앞부분이 일치하는 데이터 검색
            university_tag = UniversityTag.objects.filter(university_name__startswith=universities)

        if not university_tag.exists():
            return Response({'error': 'No matching universities found.'})

        # 데이터를 직렬화하고, 배열 형태로 반환
        serializer = self.get_serializer(university_tag, many=True)
        university_list = [university["university_name"] for university in serializer.data]
        return Response({"university": university_list})

# 플랫폼 목록을 출력하는 viewset
class PlatformViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
        
    def get_queryset(self):
        return Platform.objects.all()
    
    def get_serializer_class(self):
        return PlatformSerializer

    def list(self, request, *args, **kwargs):
        # 기존의 list 메서드를 호출하여 data를 가져옴
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # 각 객체의 genre_name만 추출하여 리스트로 변환
        platform_list = [platform["platform_name"] for platform in serializer.data]
        # data를 배열 형태로 감싸서 반환
        return Response({"platform": platform_list})
    
    @action(detail=False, methods=['post'], url_path='input')
    def filter_by_platform(self, request):
        platforms = request.data.get('platform_name', [])
        if not platforms:
            return Response({'error': 'No platforms provided.'})

         # 입력된 stack_name이 영어인지 한글인지 확인
        if platforms.isalpha() and platforms[0].lower() in 'abcdefghijklmnopqrstuvwxyz':
            # 영어일 경우 입력된 길이만큼 대소문자 구분 없이 검색
            platform_tag = Platform.objects.filter(platform_name__istartswith=platforms)
        else:
            # 한글일 경우 입력된 길이만큼 앞부분이 일치하는 데이터 검색
            platform_tag = Platform.objects.filter(platform_name__startswith=platforms)

        if not platform_tag.exists():
            return Response({'error': 'No matching platforms found.'})

        # 데이터를 직렬화하고, 배열 형태로 반환
        serializer = self.get_serializer(platform_tag, many=True)
        platform_list = [platform["platform_name"] for platform in serializer.data]
        return Response({"platform": platform_list})
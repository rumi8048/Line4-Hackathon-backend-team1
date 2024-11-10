from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, mixins

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
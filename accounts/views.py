from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Account, UniversityTag, GenreTag
from .serializers import SignUpSerializer, UniversityTagSerializer, GenreTagSerializer
from django.http import JsonResponse 
from django.views import View  


class SignUpViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입에 성공하셨습니다"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def check_username(self, request):
        username = request.query_params.get('username')
        if User.objects.filter(username=username).exists():
            return Response({"message": "중복된 아이디가 존재합니다"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "사용 가능한 아이디입니다"})

    @action(detail=False, methods=['get'])
    def check_nickname(self, request):
        nickname = request.query_params.get('nickname')
        if Account.objects.filter(nickname=nickname).exists():
            return Response({"message": "중복된 닉네임이 존재합니다"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Nickname available"})

class UniversityTagViewSet(viewsets.ModelViewSet):
    queryset = UniversityTag.objects.all()
    serializer_class = UniversityTagSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        name = request.query_params.get('name', '')
        queryset = UniversityTag.objects.filter(university_name__icontains=name)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class GenreTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GenreTag.objects.all()
    serializer_class = GenreTagSerializer
    

class LoginView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 사용자 인증
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # 세션 생성
            return JsonResponse({'message': '로그인 성공'}, status=200)
        else:
            return JsonResponse({'message': '아이디 또는 비밀번호가 틀렸습니다'}, status=401)

class LogoutView(View):
    def post(self, request):
        logout(request)  # 세션 삭제
        return JsonResponse({'message': '로그아웃 성공'}, status=200)


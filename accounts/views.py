from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Account
from .serializers import SignUpSerializer
from django.http import JsonResponse 
from django.contrib import auth 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

class SignUpViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입에 성공하셨습니다"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def check_username(self, request):
        username = request.data.get('username')
        print(username)
        if User.objects.filter(username=username).exists():
            return Response({"message": "중복된 아이디가 존재합니다"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "사용 가능한 아이디입니다"})

    @action(detail=False, methods=['post'])
    def check_nickname(self, request):
        nickname = request.data.get('nickname')
        print(nickname)
        if Account.objects.filter(nickname=nickname).exists():
            return Response({"message": "중복된 닉네임이 존재합니다"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "사용 가능한 닉네임입니다"})
    

class LoginView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @method_decorator(csrf_exempt)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # 사용자 인증
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)  # 세션 생성
            return JsonResponse({'message': '로그인 성공'}, status=200)
        else:
            return JsonResponse({'message': '아이디 또는 비밀번호가 틀렸습니다'}, status=401)

class LogoutView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @method_decorator(csrf_exempt)
    def get(self, request):
        print(request)
        auth.logout(request)  # 세션 삭제
        return JsonResponse({'message': '로그아웃 성공'})
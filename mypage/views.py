from rest_framework import mixins, viewsets
from accounts.models import Account
from .serializers import AccountCollaborateProjectSerializer, AccountInfoSerializer, AccountScrapProjectSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class AccountViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    serializer_class = AccountInfoSerializer
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_queryset(self):
        return Account.objects.all()
    
    @action(detail=False, methods=['GET'], url_path='me')
    def me(self, request):
        account = self.get_queryset().filter(user=request.user).first()
        if account:
            serializer = self.get_serializer(account)
            return Response(serializer.data)
        return Response({"detail": "Account not found."}, status=404)

class AccountCollaborateProjectViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = AccountCollaborateProjectSerializer
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_queryset(self):
        return Account.objects.all()
    
    def list(self, request):
        account = self.get_queryset().filter(user=request.user).first()
        print(account)
        if account:
            serializer = self.get_serializer(account)
            return Response(serializer.data)
        return Response({"detail": "Account not found."})

class AccountScrapProjectViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = AccountScrapProjectSerializer
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_queryset(self):
        return Account.objects.all()
    
    def list(self, request):
        account = self.get_queryset().filter(user=request.user).first()
        if account:
            serializer = self.get_serializer(account)
            return Response(serializer.data)
        return Response({"detail": "Account not found."}, status=404)
    
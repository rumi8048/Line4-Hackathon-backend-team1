from rest_framework.permissions import BasePermission, SAFE_METHODS

from ptn_project.models import CollaboratorMiddleTable

class IsProjectOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # 슈퍼유저인지 확인
        if request.user.is_superuser:
            return True
        # 프로젝트의 협력자인지 확인
        return CollaboratorMiddleTable.objects.filter(project=obj, account__user=request.user).exists()
    
class IsCommentOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.writer == request.user or request.user.is_superuser
    
class IsPossibleCommentsOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
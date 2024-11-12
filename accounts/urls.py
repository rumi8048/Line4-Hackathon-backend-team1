from django.urls import include, path
from .views import SignUpViewSet, LoginView,LogoutView
from rest_framework import routers
from .views import FindUserViewSet

finduser_router = routers.SimpleRouter(trailing_slash=False)
finduser_router.register("", FindUserViewSet, basename="finduser")

urlpatterns = [
    path('signup/', SignUpViewSet.as_view({'post': 'register'})),
    path('check-duplicate-id/', SignUpViewSet.as_view({'post': 'check_username'})),
    path('check-duplicate-nickname/', SignUpViewSet.as_view({'post': 'check_nickname'})),
    path('login/', LoginView.as_view({'post': 'login'})),
    path('logout/', LogoutView.as_view({'get': 'logout'})),
    path('', include(finduser_router.urls)),
]
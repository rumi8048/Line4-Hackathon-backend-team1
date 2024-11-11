from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignUpViewSet, UniversityTagViewSet, GenreTagViewSet,LoginView,LogoutView

router = DefaultRouter()
router.register(r'search/universities', UniversityTagViewSet, basename='university')
router.register(r'search/genres', GenreTagViewSet, basename='genre')

urlpatterns = [
    path('signup/', SignUpViewSet.as_view({'post': 'register'})),
    path('check-duplicate-id/', SignUpViewSet.as_view({'get': 'check_username'})),
    path('check-duplicate-nickname/', SignUpViewSet.as_view({'get': 'check_nickname'})),
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

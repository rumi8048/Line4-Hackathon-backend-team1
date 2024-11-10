from django.urls import include, path
from .views import *
from rest_framework import routers

app_name = 'ptn_project'

project_router = routers.SimpleRouter(trailing_slash=False)
project_router.register("", ProjectViewSet, basename="project")

genreproject_router = routers.SimpleRouter(trailing_slash=False)
genreproject_router.register("filter", GenreProjectViewSet, basename="filter")

finduser_router = routers.SimpleRouter(trailing_slash=False)
finduser_router.register("finduser", FindUserViewSet, basename="finduser")
urlpatterns = [
  path('', include(project_router.urls)),
  path('', include(finduser_router.urls)),
  path('', include(genreproject_router.urls)),
]

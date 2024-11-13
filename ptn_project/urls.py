from django.urls import include, path
from .views import *
from rest_framework import routers

app_name = 'ptn_project'

project_router = routers.SimpleRouter(trailing_slash=False)
project_router.register("", ProjectViewSet, basename="project")

home_router = routers.SimpleRouter(trailing_slash=False)
home_router.register("home", HomeProjectViewSet, basename="home")

urlpatterns = [
  path('', include(project_router.urls)),
  path('', include(home_router.urls)),
]

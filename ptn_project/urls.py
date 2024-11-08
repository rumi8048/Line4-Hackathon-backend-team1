from django.urls import include, path
from .views import *
from rest_framework import routers

app_name = 'ptn_project'
project_router = routers.SimpleRouter(trailing_slash=False)
project_router.register("project", ProjectViewSet, basename="project")

urlpatterns = [
  path('', include(project_router.urls)),
]
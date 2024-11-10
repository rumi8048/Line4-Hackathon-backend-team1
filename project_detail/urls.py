from django.urls import include, path
from .views import *
from rest_framework import routers

app_name = 'project_detail'
project_router = routers.SimpleRouter(trailing_slash=False)
project_router.register("", ProjectDetailViewSet, basename="project_detail")

urlpatterns = [
  path('', include(project_router.urls)),
]
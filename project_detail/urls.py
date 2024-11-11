from django.urls import include, path
from .views import *
from rest_framework import routers

app_name = 'project_detail'
project_router = routers.SimpleRouter(trailing_slash=False)
project_router.register("", ProjectDetailViewSet, basename="project_detail")

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register("comment", CommentViewSet, basename="comment")

comment_detail_router = routers.SimpleRouter(trailing_slash=False)
comment_detail_router.register("comment", DetailCommentViewSet, basename="comment")

in_comment_router = routers.SimpleRouter(trailing_slash=False)
in_comment_router.register("in_comment", InCommentViewSet, basename="in_comment")

in_comment_detail_router = routers.SimpleRouter(trailing_slash=False)
in_comment_detail_router.register("in_comment", DetailInCommentViewSet, basename="in_comment")

urlpatterns = [
  path('', include(project_router.urls)),
  path('<int:project_id>/', include(comment_router.urls)),
  path('<int:project_id>/', include(comment_detail_router.urls)),
  path('<int:project_id>/comment/<int:comment_id>/', include(in_comment_router.urls)),
  path('<int:project_id>/comment/<int:comment_id>/', include(in_comment_detail_router.urls)),
]
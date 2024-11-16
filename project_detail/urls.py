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

discussion_router = routers.SimpleRouter(trailing_slash=False)
discussion_router.register("discussion", DiscussionViewSet, basename="discussion")

discussion_detail_router = routers.SimpleRouter(trailing_slash=False)
discussion_detail_router.register("discussion", DetailDiscussionViewSet, basename="discussion")

feedback_router = routers.SimpleRouter(trailing_slash=False)
feedback_router.register("feedback", FeedbackViewSet, basename="feedback")

adopt_feedback_router = routers.SimpleRouter(trailing_slash=False)
adopt_feedback_router.register("adopt_feedback", AdoptFeedbackViewSet, basename="adopt_feedback")

feedback_detail_router = routers.SimpleRouter(trailing_slash=False)
feedback_detail_router.register("feedback", DetailFeedbackViewSet, basename="feedback")

ai_summary_router = routers.SimpleRouter(trailing_slash=False)
ai_summary_router.register("ai_summary", AiSummaryViewSet, basename="ai_summary")

urlpatterns = [
  path('', include(project_router.urls)),
  path('<int:project_id>/', include(comment_router.urls)),
  path('<int:project_id>/', include(comment_detail_router.urls)),
  path('<int:project_id>/comment/<int:comment_id>/', include(in_comment_router.urls)),
  path('<int:project_id>/comment/<int:comment_id>/', include(in_comment_detail_router.urls)),
  path('<int:project_id>/', include(discussion_router.urls)),
  path('<int:project_id>/', include(discussion_detail_router.urls)),
  path('<int:project_id>/', include(feedback_router.urls)),
  path('<int:project_id>/', include(adopt_feedback_router.urls)),
  path('<int:project_id>/', include(feedback_detail_router.urls)),
  path('<int:project_id>/', include(ai_summary_router.urls)),
]
from django.urls import include, path
from .views import *
from rest_framework import routers


app_name = 'search'

genretag_router = routers.SimpleRouter(trailing_slash=False)
genretag_router.register("genre", GenreViewSet, basename="genre")

stacktag_router = routers.SimpleRouter(trailing_slash=False)
stacktag_router.register("stack", StackViewSet, basename="stack")

universitytag_router = routers.SimpleRouter(trailing_slash=False)
universitytag_router.register("university", UniversityViewSet, basename="university")

platformtag_router = routers.SimpleRouter(trailing_slash=False)
platformtag_router.register("platform", PlatformViewSet, basename="platform")

urlpatterns = [
    path('', include(genretag_router.urls)),
    path('', include(stacktag_router.urls)),
    path('', include(universitytag_router.urls)),
    path('', include(platformtag_router.urls)),
]
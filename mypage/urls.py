from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'my_page'

account_router = routers.SimpleRouter(trailing_slash=False)
account_router.register("accountinfo", AccountViewSet, basename="accountinfo")

account_collaborate_project_router = routers.SimpleRouter(trailing_slash=False)
account_collaborate_project_router.register("collaborateproject", AccountCollaborateProjectViewSet, basename="collaborateproject")

account_scrap_project_router = routers.SimpleRouter(trailing_slash=False)
account_scrap_project_router.register("scrapproject", AccountScrapProjectViewSet, basename="scrapproject")

urlpatterns = [
    path('', include(account_router.urls)),
    path('', include(account_collaborate_project_router.urls)),
    path('', include(account_scrap_project_router.urls)),
]
from django.urls import path
from .views import SignUpViewSet, LoginView,LogoutView

urlpatterns = [
    path('signup/', SignUpViewSet.as_view({'post': 'register'})),
    path('check-duplicate-id/', SignUpViewSet.as_view({'post': 'check_username'})),
    path('check-duplicate-nickname/', SignUpViewSet.as_view({'post': 'check_nickname'})),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
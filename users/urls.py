
from django.urls import path, include
from .views import RegisterUserView, CustomLoginView, CustomLogoutView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('registration/', RegisterUserView.as_view(), name='project'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
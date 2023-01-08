
from django.urls import path, include
from .views import RegisterUserView, CustomLoginView, CustomLogoutView, activate, activate_info
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('registration/', RegisterUserView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('activating/', activate_info, name='activate-info'),
]
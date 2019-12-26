from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import (
    RegisterView,
    LoginView,
    ValidationView,
    DashboardView)

urlpatterns = [
    path('', DashboardView.as_view(), name='person'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('validation/', ValidationView.as_view(), name='validation'),
]

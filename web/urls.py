from django.urls import path, include

from web.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]

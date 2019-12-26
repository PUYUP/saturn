from django.urls import path, include

# THIRD PARTY
from rest_framework.routers import DefaultRouter

from .general.views import CategoryApiView
from .topic.views import TopicApiView
from .group.views import AccessGroupView, AccessMemberView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('categories', CategoryApiView, basename='category')
router.register('topics', TopicApiView, basename='topic')
router.register('access-groups', AccessGroupView, basename='access_group')
router.register('access-members', AccessMemberView, basename='access_member')

app_name = 'debate'

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include((router.urls, 'debate'), namespace='debates')),
]

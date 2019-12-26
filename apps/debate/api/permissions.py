from uuid import UUID
from pprint import pprint

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions

# PROJECTS UTILS
from utils.generals import get_model

Topic = get_model('debate', 'Topic')


class IsCreatorOrReject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        person = getattr(request.user, 'person', None)

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `creator`.
        return obj.creator == person


class IsAllowOrReject(permissions.BasePermission):
    def has_permission(self, request, view):
        basename = getattr(view, 'basename', None)
        basename_clean = basename.replace('_', '')

        if (
            request.user.has_perm('debate.add_%s' % basename_clean) and
            request.user.has_perm('debate.change_%s' % basename_clean) and
            request.user.has_perm('debate.delete_%s' % basename_clean)
        ):
            return True
        return False

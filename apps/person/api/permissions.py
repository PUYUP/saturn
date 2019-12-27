from uuid import UUID

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions

# PROJECTS UTILS
from utils.generals import get_model

AttributeValue = get_model('person', 'AttributeValue')


class IsAllowUpdateObject(permissions.BasePermission):
    def has_permission(self, request, view):
        basename = getattr(view, 'basename', None)
        basename_clean = basename.replace('_', '')

        if hasattr(request.user, 'person'):
            if (
                request.user.has_perm('person.add_%svalue' % basename_clean) and
                request.user.has_perm('person.change_%svalue' % basename_clean) and
                request.user.has_perm('person.delete_%svalue' % basename_clean)
            ):
                return True
        return False


class IsOwnerOrReject(permissions.BasePermission):
    """
    Validate current user is self
    If not access read only
    """

    def has_permission(self, request, view):
        # Staff can always access CRUD
        if request.user.is_staff:
            return True

        # Only as person allowed
        if hasattr(request.user, 'person'):
            user_uuid = request.user.person.uuid
            current_uuid = view.kwargs['uuid']

            try:
                current_uuid = UUID(current_uuid)
            except ValueError:
                return False
            return current_uuid == user_uuid
        return False

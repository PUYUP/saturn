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

        if hasattr(request.user, 'person'):
            if (request.user.has_perm('person.add_%svalue' % basename) and
                    request.user.has_perm('person.change_%svalue' % basename)):
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


class IsEntityOwnerOrReject(permissions.BasePermission):
    """Entity Permission"""

    def has_permission(self, request, view):
        # Staff can always access CRUD
        if request.user.is_staff:
            return True

        # Only as person allowed
        person = getattr(request.user, 'person', None)
        if person:
            entity_type = ContentType.objects.get_for_model(person)

            if request.method == 'DELETE':
                entity_uuid = request.GET.get('uuid', None)

            try:
                entity_uuid = UUID(entity_uuid)
            except ValueError:
                return False

            try:
                AttributeValue.objects.get(
                    uuid=entity_uuid, object_id=person.pk,
                    content_type=entity_type)
            except ObjectDoesNotExist:
                return False
            return True
        return False

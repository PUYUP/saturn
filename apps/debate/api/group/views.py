from uuid import UUID

from django.db.models import Q, Case, When, Value, CharField, Count
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache

# THIRD PARTY
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status as response_status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound

# SERIALIZERS
from .serializers import AccessGroupSerializer, AccessMemberSerializer

# GET MODELS FROM GLOBAL UTILS
from utils.generals import get_model

# LOCAL PERMISSIONS
from ..permissions import IsAllowOrReject, IsCreatorOrReject

AccessGroup = get_model('debate', 'AccessGroup')
AccessMember = get_model('debate', 'AccessMember')

# Define to avoid used ...().paginate__
PAGINATOR = PageNumberPagination()


class AccessGroupView(viewsets.ViewSet):
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated,)
    permission_action = {
        # Disable update if not owner
        'create': [IsAllowOrReject],
        'partial_update': [IsAuthenticated, IsAllowOrReject, IsCreatorOrReject],
        'destroy': [IsAuthenticated, IsAllowOrReject, IsCreatorOrReject],
    }

    def get_permissions(self):
        """
        Instantiates and returns
        the list of permissions that this view requires.
        """
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_action
                    [self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def list(self, request, format=None):
        response = dict()
        context = {'request': self.request}
        show = request.query_params.get('show', None)
        person = getattr(request.user, 'person', None)

        # Querying
        queryset = AccessGroup.objects \
            .prefetch_related('creator', 'creator__user') \
            .select_related('creator', 'creator__user') \
            .filter(creator=person) \
            .annotate(num_members=Count('access_members'))

        # With pagination
        if show != 'all':
            # Create paginator
            queryset_paginator = PAGINATOR.paginate_queryset(queryset, request)
            serializer = AccessGroupSerializer(queryset_paginator, many=True, context=context)

            # Prepare a responses with some params
            response['count'] = PAGINATOR.page.paginator.count
            response['total_page'] = PAGINATOR.page.paginator.num_pages
            response['current'] = PAGINATOR.page.number
            response['navigate'] = {
                'previous': PAGINATOR.get_previous_link(),
                'next': PAGINATOR.get_next_link()
            }

            response['results'] = serializer.data
            return Response(response, status=response_status.HTTP_200_OK)
        
        # Show all's
        serializer = AccessGroupSerializer(queryset, many=True, context=context)
        return Response(serializer.data, status=response_status.HTTP_200_OK)

    def retrieve(self, request, uuid=None, format=None):
        context = {'request': self.request}
        person = getattr(request.user, 'person', None)

        if uuid and type(uuid) is not UUID:
            try:
                uuid = UUID(uuid)
            except ValueError:
                raise NotFound()

        try:
            queryset = AccessGroup.objects \
                .prefetch_related('creator', 'creator__user') \
                .select_related('creator', 'creator__user') \
                .get(uuid=uuid, creator=person)
        except ObjectDoesNotExist:
            raise NotFound()

        serializer = AccessGroupSerializer(queryset, many=False, context=context)
        return Response(serializer.data, status=response_status.HTTP_200_OK)

    @method_decorator(never_cache)
    @transaction.atomic
    def create(self, request, format=None):
        context = {'request': self.request}
        serializer = AccessGroupSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=response_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=response_status.HTTP_400_BAD_REQUEST)

    @method_decorator(never_cache)
    @transaction.atomic
    def partial_update(self, request, uuid=None, format=None):
        """Update a item... """
        context = {'request': self.request}
        
        if uuid and type(uuid) is not UUID:
            try:
                uuid = UUID(uuid)
            except ValueError:
                raise NotFound()

        try:
            queryset = AccessGroup.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            raise NotFound()

        # Check permissions
        self.check_object_permissions(request, queryset)

        serializer = AccessGroupSerializer(
            instance=queryset,
            data=request.data,
            context=context,
            partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=response_status.HTTP_200_OK)
        return Response(serializer.errors, status=response_status.HTTP_400_BAD_REQUEST)

    @method_decorator(never_cache)
    @transaction.atomic
    def destroy(self, request, uuid=None, format=None):
        if uuid and type(uuid) is not UUID:
            try:
                uuid = UUID(uuid)
            except ValueError:
                raise NotFound()

        try:
            queryset = AccessGroup.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            raise NotFound()

        queryset.delete()
        return Response({'detail': _("Berhasil dihapus.")},
            status=response_status.HTTP_204_NO_CONTENT)


class AccessMemberView(viewsets.ViewSet):
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated,)
    permission_action = {
        # Disable update if not owner
        'create': [IsAllowOrReject],
        'partial_update': [IsAuthenticated, IsAllowOrReject],
        'destroy': [IsAuthenticated, IsAllowOrReject],
    }

    def get_permissions(self):
        """
        Instantiates and returns
        the list of permissions that this view requires.
        """
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_action
                    [self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def list(self, request, format=None):
        response = dict()
        context = {'request': self.request}
        group_uuid = request.query_params.get('group_uuid', None)

        if group_uuid and type(group_uuid) is not UUID:
            try:
                group_uuid = UUID(group_uuid)
            except ValueError:
                raise NotFound()

        # Querying
        queryset = AccessMember.objects \
            .prefetch_related('access_group', 'access_group__creator') \
            .select_related('access_group', 'access_group__creator') \
            .filter(access_group__uuid=group_uuid)

        # Create paginator
        queryset_paginator = PAGINATOR.paginate_queryset(queryset, request)
        serializer = AccessMemberSerializer(queryset_paginator, many=True, context=context)

        # Prepare a responses with some params
        response['count'] = PAGINATOR.page.paginator.count
        response['total_page'] = PAGINATOR.page.paginator.num_pages
        response['current'] = PAGINATOR.page.number
        response['navigate'] = {
            'previous': PAGINATOR.get_previous_link(),
            'next': PAGINATOR.get_next_link()
        }

        response['results'] = serializer.data
        return Response(response, status=response_status.HTTP_200_OK)

    @method_decorator(never_cache)
    @transaction.atomic
    def create(self, request, format=None):
        context = {'request': self.request}
        serializer = AccessMemberSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=response_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=response_status.HTTP_400_BAD_REQUEST)

    @method_decorator(never_cache)
    @transaction.atomic
    def partial_update(self, request, uuid=None, format=None):
        """Update a item... """
        context = {'request': self.request}
        
        if uuid and type(uuid) is not UUID:
            try:
                uuid = UUID(uuid)
            except ValueError:
                raise NotFound()

        try:
            queryset = AccessMember.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            raise NotFound()

        # Check permissions
        self.check_object_permissions(request, queryset)

        serializer = AccessMemberSerializer(
            instance=queryset,
            data=request.data,
            context=context,
            partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=response_status.HTTP_200_OK)
        return Response(serializer.errors, status=response_status.HTTP_400_BAD_REQUEST)

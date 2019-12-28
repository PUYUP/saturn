from uuid import UUID

from django.db.models import Q, Case, When, Value, CharField
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
from .serializers import TopicSerializer

# GET MODELS FROM GLOBAL UTILS
from utils.generals import get_model

# LOCAL UTILS
from ...utils.constant import (
    PUBLIC, PRIVATE, DRAFT, PUBLISHED, STATUS_CHOICES, ACCESS_CHOICES)

# LOCAL PERMISSIONS
from ..permissions import IsAllowOrReject, IsCreatorOrReject

# PERSON PERMISSIONS
from ....person.api.permissions import IsAccountValidated

Category = get_model('debate', 'Category')
Topic = get_model('debate', 'Topic')

# Define to avoid used ...().paginate__
PAGINATOR = PageNumberPagination()


class TopicApiView(viewsets.ViewSet):
    lookup_field = 'uuid'
    permission_classes = (AllowAny,)
    permission_action = {
        # Disable update if not owner
        'create': [IsAuthenticated, IsAccountValidated, IsAllowOrReject],
        'partial_update': [IsAuthenticated, IsAccountValidated, IsAllowOrReject, IsCreatorOrReject],
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
        creator_uuid = request.query_params.get('creator_uuid', None)
        status = request.query_params.get('status', None)
        person = getattr(request.user, 'person', None)

        if creator_uuid and type(creator_uuid) is not UUID:
            try:
                creator_uuid = UUID(creator_uuid)
            except ValueError:
                raise NotFound()

        # Querying
        q_status = Q(status=PUBLISHED)
        q_access = Q(access=PUBLIC)
        queryset = Topic.objects \
            .prefetch_related('creator', 'creator__user', 'category', 'access_group') \
            .select_related('creator', 'creator__user', 'category')

        # Current loggedin person
        # Show all topics
        if person and person.uuid == creator_uuid:
            q_status = Q()
            q_access = Q()

            if status:
                q_status = Q(status=status)

        # From creator only
        if creator_uuid:
            queryset = queryset.filter(creator__uuid=creator_uuid)

        # Perfom more filter...
        queryset = queryset.filter(
            q_access,
            q_status)

        # Create paginator
        queryset_paginator = PAGINATOR.paginate_queryset(queryset, request)
        serializer = TopicSerializer(queryset_paginator, many=True, context=context)

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

    def retrieve(self, request, uuid=None, format=None):
        context = {'request': self.request}
        person = getattr(request.user, 'person', None)
        person_uuid = getattr(person, 'uuid', None)

        if uuid and type(uuid) is not UUID:
            try:
                uuid = UUID(uuid)
            except ValueError:
                raise NotFound()

        status_for_creator = list()
        for item in STATUS_CHOICES:
            status = item[0]
            status_when = When(Q(creator__uuid=person_uuid) & Q(status=status), then=Value(status))
            status_for_creator.append(status_when)

        try:
            queryset = Topic.objects \
                .prefetch_related('creator', 'creator__user', 'category', 'access_group') \
                .select_related('creator', 'creator__user', 'category') \
                .get(
                    uuid=uuid,
                    status=Case(
                        *status_for_creator,
                        output_field=CharField(),
                        default=Value(PUBLISHED)
                    ))
        except ObjectDoesNotExist:
            raise NotFound()

        serializer = TopicSerializer(queryset, many=False, context=context)
        return Response(serializer.data, status=response_status.HTTP_200_OK)

    @method_decorator(never_cache)
    @transaction.atomic
    def create(self, request, format=None):
        context = {'request': self.request}
        serializer = TopicSerializer(data=request.data, context=context)
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
            queryset = Topic.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            raise NotFound()

        # Check permissions
        self.check_object_permissions(request, queryset)

        serializer = TopicSerializer(
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
            queryset = Topic.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            raise NotFound()

        queryset.delete()
        return Response({'detail': _("Berhasil dihapus.")},
            status=response_status.HTTP_204_NO_CONTENT)
    
from uuid import UUID

from django.db.models import F, Subquery, OuterRef
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.core.exceptions import (
    ObjectDoesNotExist, ValidationError as CoreValidationError)
from django.views.decorators.cache import never_cache
from django.contrib.contenttypes.models import ContentType

# THIRD PARTY
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import (
    FormParser, FileUploadParser, MultiPartParser)
from rest_framework import status as response_status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, NotAcceptable, ValidationError

# SERIALIZERS
from .serializers import CategorySerializer

# GET MODELS FROM GLOBAL UTILS
from utils.generals import get_model

Category = get_model('debate', 'Category')


class CategoryApiView(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request, format=None):
        context = {'request': self.request}
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True, context=context)
        return Response(serializer.data, status=response_status.HTTP_200_OK)

from django.db import transaction
from django.db.models import F, Exists, OuterRef
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

# THIRD PARTY
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status as response_status
from rest_framework.exceptions import NotAcceptable, ValidationError, NotFound

from utils.generals import get_model

Category = get_model('debate', 'Category')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('slug', 'date_created', 'date_updated',)

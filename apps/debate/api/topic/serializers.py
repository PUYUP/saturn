from django.db import transaction

# THIRD PARTY
from rest_framework import serializers
from rest_framework import status as response_status

from utils.generals import get_model
from ...utils.auths import CurrentPersonDefault

Category = get_model('debate', 'Category')
Topic = get_model('debate', 'Topic')


class TopicSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=CurrentPersonDefault())
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    access_display = serializers.CharField(source='get_access_display', read_only=True)
    category_display = serializers.CharField(source='category.label', read_only=True)
    creator_uuid = serializers.CharField(source='creator.uuid', read_only=True)
    creator_name = serializers.CharField(source='creator.user.username', read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='debates:topic-detail', lookup_field='uuid', read_only=True)

    class Meta:
        model = Topic
        exclude = ('id',)

    @transaction.atomic
    def create(self, validated_data):
        return Topic.objects.create(**validated_data)

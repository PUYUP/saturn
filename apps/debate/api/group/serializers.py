from django.db import transaction, IntegrityError

# THIRD PARTY
from rest_framework import serializers
from rest_framework import status as response_status

from utils.generals import get_model
from ...utils.auths import CurrentPersonDefault

AccessGroup = get_model('debate', 'AccessGroup')
AccessMember = get_model('debate', 'AccessMember')


class AccessMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessMember
        exclude = ('date_created', 'date_updated',)

    @transaction.atomic
    def create(self, validated_data):
        return AccessMember.objects.create(**validated_data)


class AccessGroupSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=CurrentPersonDefault())
    url = serializers.HyperlinkedIdentityField(
        view_name='debates:access_group-detail', lookup_field='uuid', read_only=True)
    members = serializers.CharField(required=False)
    num_members = serializers.IntegerField(read_only=True)

    class Meta:
        model = AccessGroup
        exclude = ('date_created', 'date_updated',)
        extra_kwargs = {
            'creator': {
                'write_only': True
            },
            'access_members': {
                'write_only': True
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        return AccessGroup.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        members = validated_data.get('members', None)
        if members:
            members_list_obj = list()
            members_list = members.split(',')
            for item in members_list:
                member_obj = AccessMember(access_group=instance, member=item)
                members_list_obj.append(member_obj)

            # Bulk create members
            AccessMember.objects.bulk_create(members_list_obj, ignore_conflicts=True)

        instance.label = validated_data.get('label', instance.label)
        instance.save()
        return instance

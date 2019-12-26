import uuid

from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _

# LOCAL UTILS
from apps.debate.utils.constant import (
    DRAFT, STATUS_CHOICES, PUBLIC, ACCESS_CHOICES)


# 0
class AbstractTopic(models.Model):
    creator = models.ForeignKey(
        'person.Person',
        on_delete=models.SET_NULL, null=True,
        related_name='topics')
    category = models.ForeignKey(
        'debate.Category',
        on_delete=models.SET_NULL, null=True,
        related_name='topics')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=355)
    description = models.TextField()
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=100, default=DRAFT)
    access = models.CharField(
        choices=ACCESS_CHOICES, max_length=100, default=PUBLIC)
    access_group = models.ManyToManyField(
        'debate.AccessGroup',
        related_name='topics', blank=True)
    opened_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    # Generic relations
    tags = GenericRelation('debate.Tag')
    votes = GenericRelation('debate.Vote')
    attachments = GenericRelation('debate.Attachment')

    response_count = models.IntegerField(
        null=True, blank=True, editable=False)
    vote_up_count = models.IntegerField(
        null=True, blank=True, editable=False)
    vote_down_count = models.IntegerField(
        null=True, blank=True, editable=False)

    class Meta:
        abstract = True
        app_label = 'debate'
        unique_together = ('label', 'creator',)
        ordering = ('-date_created',)
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    def __str__(self):
        return self.label


# 1
class AbstractResponse(models.Model):
    topic = models.ForeignKey(
        'debate.Topic',
        on_delete=models.SET_NULL, null=True,
        related_name='responses')
    creator = models.ForeignKey(
        'person.Person',
        on_delete=models.SET_NULL, null=True,
        related_name='responses')
    response_to = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='responses')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=355, null=True, blank=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    # Generic relations
    tags = GenericRelation('debate.Tag')
    votes = GenericRelation('debate.Vote')
    attachments = GenericRelation('debate.Attachment')

    vote_up_count = models.IntegerField(
        null=True, blank=True, editable=False)
    vote_down_count = models.IntegerField(
        null=True, blank=True, editable=False)

    class Meta:
        abstract = True
        app_label = 'debate'
        ordering = ('-date_created',)
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")

    def __str__(self):
        return self.label


# 2
class AbstractDiscussed(models.Model):
    topic = models.ForeignKey(
        'debate.Topic',
        on_delete=models.CASCADE,
        related_name='discusseds')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        app_label = 'debate'
        verbose_name = _("Discussed")
        verbose_name_plural = _("Discusseds")

    def __str__(self):
        return self.topic.label

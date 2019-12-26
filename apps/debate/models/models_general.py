import uuid

from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

# LOCAL UTILS
from apps.debate.utils.files import (
    directory_file_path,
    directory_image_path)


# 0
class AbstractCategory(models.Model):
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='childs',
        limit_choices_to={'parent__isnull': True})
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=255)
    slug = models.SlugField(editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'debate'
        unique_together = ('label',)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.label
    
    def save(self, *args, **kwargs):
        # Auto create slug from label
        if self.label:
            self.slug = slugify(self.label)

        super().save(*args, **kwargs)


# 1
class AbstractTag(models.Model):
    creator = models.ForeignKey(
        'person.Person', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='tags')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=255)
    slug = models.SlugField(editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Generic relations
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        limit_choices_to=Q(app_label='debate'))
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        app_label = 'debate'
        unique_together = ('label',)
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.label
    
    def save(self, *args, **kwargs):
        # Auto create slug from label
        if self.label:
            self.slug = slugify(self.label)

        super().save(*args, **kwargs)


# 2
class AbstractVote(models.Model):
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    VOTE_TYPES = (
        (UP_VOTE, _("Up Vote")),
        (DOWN_VOTE, _("Down Vote")),
    )

    vote_type = models.CharField(max_length=1, choices=VOTE_TYPES)
    creator = models.ForeignKey(
        'person.Person', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='votes')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Generic relations
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        limit_choices_to=Q(app_label='debate'))
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        app_label = 'debate'
        unique_together = ('object_id', 'creator',)
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")

    def __str__(self):
        return self.get_vote_type_display


# 3
class AbstractAttachment(models.Model):
    """General attachment used for various objects"""
    creator = models.ForeignKey(
        'person.Person',
        on_delete=models.SET_NULL,
        null=True, blank=True, related_name='attachments')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    value_image = models.ImageField(
        upload_to=directory_image_path,
        max_length=500, null=True, blank=True)
    value_file = models.FileField(
        upload_to=directory_file_path,
        max_length=500, null=True, blank=True)
    featured = models.BooleanField(null=True)
    caption = models.TextField(max_length=500, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    # Generic relations
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        limit_choices_to=Q(app_label='debate'))
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        app_label = 'debate'
        ordering = ('-date_updated',)
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __str__(self):
        value = None

        if self.value_image:
            value = self.value_image.url

        if self.value_file:
            value = self.value_file.url

        return value


# 4
class AbstractAccessGroup(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=355)
    creator = models.ForeignKey(
        'person.Person',
        on_delete=models.SET_NULL, null=True,
        related_name='access_groups')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        app_label = 'debate'
        ordering = ('-date_created',)
        verbose_name = _("Access Group")
        verbose_name_plural = _("Access Groups")

    def __str__(self):
        return self.label


# 5
class AbstractAccessMember(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    access_group = models.ForeignKey(
        'debate.AccessGroup',
        on_delete=models.SET_NULL,
        related_name='access_members',
        null=True, blank=True)
    member = models.CharField(max_length=255, verbose_name=_("Email or Username"))
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        app_label = 'debate'
        ordering = ('-date_created',)
        verbose_name = _("Access Member")
        verbose_name_plural = _("Access Members")
        unique_together = ('access_group', 'member',)

    def __str__(self):
        return self.member

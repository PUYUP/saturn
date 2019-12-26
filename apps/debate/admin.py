from django.contrib import admin

# LOCAL UTILS
from utils.generals import get_model

Person = get_model('person', 'Person')
Category = get_model('debate', 'Category')
Tag = get_model('debate', 'Tag')
Vote = get_model('debate', 'Vote')
Attachment = get_model('debate', 'Attachment')
Topic = get_model('debate', 'Topic')
Response = get_model('debate', 'Response')
Discussed = get_model('debate', 'Discussed')
AccessMember = get_model('debate', 'AccessMember')
AccessGroup = get_model('debate', 'AccessGroup')


class TopicExtend(admin.ModelAdmin):
    model = Topic
    list_display = ('label', 'status', 'access', 'creator',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'creator':
            kwargs['queryset'] = Person.objects.prefetch_related('user') \
                .select_related('user')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('creator', 'creator__user') \
            .select_related('creator', 'creator__user')


# AccessMember inlined to Groups
class AccessMemberInlined(admin.StackedInline):
    model = AccessMember
    can_delete = False
    fk_name = 'access_group'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('access_group') \
            .select_related('access_group')


class AccessMemberExtend(admin.ModelAdmin):
    model = AccessMember

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('access_group') \
            .select_related('access_group')


class AccessGroupExtend(admin.ModelAdmin):
    model = AccessGroup
    list_display = ('label', 'creator',)
    inlines = (AccessMemberInlined,)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'creator':
            kwargs['queryset'] = Person.objects.prefetch_related('user') \
                .select_related('user')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('creator', 'creator__user') \
            .select_related('creator', 'creator__user')


# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Vote)
admin.site.register(Attachment)
admin.site.register(Topic, TopicExtend)
admin.site.register(Response)
admin.site.register(Discussed)
admin.site.register(AccessMember, AccessMemberExtend)
admin.site.register(AccessGroup, AccessGroupExtend)

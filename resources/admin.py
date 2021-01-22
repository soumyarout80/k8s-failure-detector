from django.contrib import admin
from .models import Account
from .models import Resource
from .models import Alert
from .models import User
from django.contrib import messages
from django.utils.translation import ngettext

# Register your models here.
admin.site.register(User)


# admin.site.register(Alert)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'aws_account',
        'cluster_name',
        'email_id',
        'slack_channel',
        'notification_state',
        'k8s_endpoint',
    ]

    ordering = ['aws_account']

    # readonly_fields = ['last_sent']

    class Meta:
        model = Account


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    # def make_published(self, request, queryset):
    #     updated = queryset.update(status='p')
    #     self.message_user(request, ngettext(
    #         '%d story was successfully marked as published.',
    #         '%d stories were successfully marked as published.',
    #         updated,
    #     ) % updated, messages.SUCCESS)

    list_display = [
        'aws_account',
        'uid',
        'metrics',
        'resource_type',
        'resource_name',
        'cluster_name',
        'last_updated',
        'notification_state',
        'status',
        'status_message'
    ]
    ordering = ['aws_account', 'cluster_name']
    # actions = ['make_published']
    search_fields = ['aws_account', 'resource_type', 'resource_name', 'cluster_name']
    readonly_fields = ['last_updated']
    list_filter = (
        'aws_account',
    )

    class Meta:
        model = Resource


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = [
        'aws_account',
        'cluster_name',
        'resource_type',
        'resource_name',
        'metrics',
        'alert_status',
        'limit',
        'last_sent',
        'next_schedule',
        'count'
    ]

    ordering = ['aws_account']
    readonly_fields = ['last_sent']

    class Meta:
        model = Alert

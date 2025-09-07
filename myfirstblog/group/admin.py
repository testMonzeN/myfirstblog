from django.contrib import admin
from .models import Group, Message


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_user_count')
    list_filter = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('user_list',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'group', 'date_create')
    list_filter = ('group', 'author', 'date_create')
    search_fields = ('text', 'author__username', 'group__name')
    readonly_fields = ('date_create',)

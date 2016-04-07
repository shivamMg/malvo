from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Team, TeamMember
from .forms import (
    TeamChangeForm,
    TeamCreationForm,
    TeamMemberChangeForm,
    TeamMemberCreationForm,
)


class TeamAdmin(BaseUserAdmin):
    form = TeamChangeForm
    add_form = TeamCreationForm

    list_display = ('team_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('team_name', 'lang_pref', 'password', 'coding_start_time')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('team_name', 'lang_pref', 'coding_start_time',
                'password1', 'password2')}
        ),
    )
    search_fields = ('team_name',)
    ordering = ('team_name',)
    filter_horizontal = ()


class TeamMemberAdmin(BaseUserAdmin):
    form = TeamMemberChangeForm
    add_form = TeamMemberCreationForm

    list_display = ('full_name', 'mobile_no', 'email', 'team')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('full_name', 'mobile_no', 'email', 'team')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'mobile_no', 'email', 'team')}
        ),
    )
    search_fields = ('full_name',)
    ordering = ('full_name',)
    filter_horizontal = ()


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.unregister(Group)

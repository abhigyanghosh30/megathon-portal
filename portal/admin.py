from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.db.models import Count, F

# Register your models here.
from .models import Team, Participant

class ParticipantTeamFilter(admin.SimpleListFilter):
    title = 'team status'
    parameter_name = 'team_st'

    def lookups(self, request, model_admin):
        return (
            ('unset', 'Not Formed'),
            ('set', 'Formed'),
            ('mult', 'Multiple')
        )

    def queryset(self, request, queryset):

        if self.value() == 'unset':
            return queryset.annotate(
                team_count=Count('participant1') + Count('participant2') +
                Count('participant3') +
                Count('participant4')).filter(team_count=0)
        elif self.value() == 'mult':
            return queryset.annotate(
                team_count=Count('participant1') + Count('participant2') +
                Count('participant3') +
                Count('participant4')).filter(team_count__gt=1)
        elif self.value() == 'set':
            return queryset.annotate(
            team_count=Count('participant1') + Count('participant2') +
            Count('participant3') + Count('participant4')
            ).filter(team_count=1)
        else:
            return queryset

class SubmissionFilter(admin.SimpleListFilter):
    title = 'submission status'
    parameter_name = 'sub_st'

    def lookups(self, request, model_admin):
        return (
            ('0', 'Not submitted'),
            ('1', 'Presentation'),
            ('2', 'Presenatation and Link')
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(team__presentation='')
        elif self.value() == '1':
            return queryset.exclude(team__presentation='')
        elif self.value() == '2':
            return queryset.exclude(team__presentation='', team__submission='')

class TypeFilter(admin.SimpleListFilter):
    title = 'User Type'
    parameter_name = 'type'

    def lookups(self, request, model_Admin):
        return (
            ('0', 'E-Cell'),
            ('1', 'Teams'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(team=None)
        elif self.value() == '1':
            return queryset.exclude(team=None)


class TeamInline(admin.StackedInline):
    model = Team


class CustomUserAdmin(UserAdmin):
    inlines = (TeamInline,)
    list_per_page = 50
    search_fields = ('username', 'team__participant1__name', 'team__participant2__name',
                     'team__participant3__name', 'team__participant4__name')
    list_display = ('username', 'get_problem', 'submission_status')
    list_filter =  ('is_staff', 'is_superuser', 'team__problem', SubmissionFilter, TypeFilter)


    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def get_problem(self, object):
        return object.team.problem
    get_problem.short_description = 'Problem Statement'

    def submission_status(self, object):
        if object.team.presentation:
            return True
        else:
            return False
    submission_status.boolean = True

class ParticipantAdmin(admin.ModelAdmin):

    def team_status(self, object):
        qs = object.participant1.all()
        qs = qs.union(object.participant2.all(), all=False)
        qs = qs.union(object.participant3.all(), all=False)
        qs = qs.union(object.participant4.all(), all=False)

        if len(qs) == 0:
            return 'UNSET'
        elif len(qs) > 1:
            return mark_safe('<font color="red">MULT</font>')
        else:
            return mark_safe(f'<font color="green">{qs[0].user.username}</font>')
    fields = ('name', 'email', 'phone', 'college', 'team_status')
    readonly_fields = ('team_status',)
    list_per_page = 50
    search_fields = ('name', 'email', 'phone', 'college')
    list_display = ('name', 'email', 'team_status')
    list_filter = (ParticipantTeamFilter, )



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Participant, ParticipantAdmin)

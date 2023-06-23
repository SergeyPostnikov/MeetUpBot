from django.contrib import admin
from meetup_bot.models import Meetup, Member, MemberStatus, Report, Feedback


class MeetupInline(admin.TabularInline):
    model = Report
    extra = 0


class MemberInline(admin.TabularInline):
    model = MemberStatus
    extra = 0


class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 0


@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    search_fields = [
        'theme',
        'date',
    ]
    list_display = [
        'theme',
        'date',
    ]
    inlines = [
        MeetupInline
    ]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    search_fields = [
        'meetup',
        'speaker',
        'theme',
    ]
    list_display = [
        'meetup',
        'speaker',
        'theme',
        'is_finished',
    ]
    inlines = [
        FeedbackInline,
    ]


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'tg_name',
    ]
    list_display = [
        'tg_id',
        'name',
        'tg_name',
        'job',
    ]
    inlines = [
        MemberInline
    ]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    search_fields = [
        'report',
        'member',
    ]
    list_display = [
        'report',
        'member',
        'grade',
        'is_question',
        'is_answered',
    ]


@admin.register(MemberStatus)
class MemberStatusAdmin(admin.ModelAdmin):
    search_fields = [
        'meetup',
        'member',
        'status',
        'donate_sum',
    ]
    list_display = [
        'meetup',
        'member',
        'status',
        'donate_sum',
    ]

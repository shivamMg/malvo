from django.contrib import admin

from .models import Question, InputCase


class InputCaseInline(admin.TabularInline):
    model = InputCase
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text', 'question_no']}),
    ]
    inlines = [InputCaseInline]


admin.site.register(Question, QuestionAdmin)

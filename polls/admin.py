from django.contrib import admin

from .models import Question, Choice


# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {'fields': ['creator']}),
        (None, {'fields': ['question_text']}),
        ('Description', {'fields': ['description_text']}),
        ('Date information', {'fields': ['pub_date']}),
        ('Allow multiple choices selection', {'fields': ['multiple_choice']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'multiple_choice_selection')
    list_filter = ['pub_date', 'multiple_choice']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)

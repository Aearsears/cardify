from django.contrib import admin
from .models import Answer, Question
# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date Information', {'fields': ['created_date']})
    ]
    list_display = ('id', 'question_text', 'created_date')
    list_filter = ('question_text', 'created_date')
    search_fields = ['question_text']


class AnswerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['answer_text', 'question']}),
        ('Date Information', {'fields': ['created_date']})
    ]
    list_display = ('id', 'answer_text', 'question', 'created_date')
    list_filter = ('answer_text', 'created_date')
    search_fields = ['answer_text']


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)

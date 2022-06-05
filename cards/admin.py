from django.contrib import admin
from .models import Answer, Card, Question
# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
    ]
    list_display = ('id', 'question_text', 'created_date')
    list_filter = ('question_text', 'created_date')
    search_fields = ['question_text']


class AnswerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['answer_text', 'question']}),
    ]
    list_display = ('id', 'answer_text', 'question', 'created_date')
    list_filter = ('answer_text', 'created_date')
    search_fields = ['answer_text']


class CardAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question', 'answer', 'deck']}),
    ]
    list_display = ('id', 'question', 'answer', 'deck', 'created_date')
    list_filter = ('answer', 'created_date')
    search_fields = ['answer']


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Card, CardAdmin)

from django.contrib import admin
from .models import Tag, Question, Answer, QuestionLike, AnswerLike

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ('likes_count',)
    # для больших объёмов можно добавить raw_id_fields = ('question',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'likes_count', 'created_at')
    search_fields = ('title', 'text')
    list_filter = ('tags', 'created_at')
    filter_horizontal = ('tags',)
    inlines = (AnswerInline,)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'likes_count', 'is_correct')
    search_fields = ('text',)
    raw_id_fields = ('question', 'author')

@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created_at')

@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer', 'created_at')

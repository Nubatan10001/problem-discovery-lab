from django.contrib import admin

from .models import ConversationMessage, ProblemIdea


class ConversationInline(admin.TabularInline):
    model = ConversationMessage
    extra = 0
    readonly_fields = ['created_at']


@admin.register(ProblemIdea)
class ProblemIdeaAdmin(admin.ModelAdmin):
    list_display = ['display_title', 'owner', 'category', 'status', 'updated_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'raw_memo', 'core_problem', 'mvp_plan', 'research_theme']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ConversationInline]


@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ['idea', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['content']

# Register your models here.

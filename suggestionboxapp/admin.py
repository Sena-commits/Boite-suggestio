from django.contrib import admin

from .models import Category, Suggestion, Vote, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'description': ('name',)}

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'priority', 'is_anonymous', 'votes_count', 'views_count', 'created_at']
    list_filter = ['status', 'priority', 'category', 'is_anonymous', 'created_at']
    search_fields = ['title', 'description', 'tracking_code']
    readonly_fields = ['tracking_code', 'votes_count', 'views_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'description', 'category', 'author')
        }),
        ('Statut et priorité', {
            'fields': ('status', 'priority', 'assigned_to')
        }),
        ('Anonymat', {
            'fields': ('is_anonymous', 'tracking_code', 'anonymous_email', 'can_edit_until')
        }),
        ('Métriques', {
            'fields': ('votes_count', 'views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category', 'assigned_to')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'suggestion', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['user__username', 'suggestion__title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'suggestion', 'is_internal', 'created_at']
    list_filter = ['is_internal', 'created_at']
    search_fields = ['content', 'author__username', 'suggestion__title']
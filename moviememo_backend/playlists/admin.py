from django.contrib import admin
from .models import Playlists

@admin.register(Playlists)
class PlaylistsAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['name', 'description', 'user__username', 'user__email']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'user')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

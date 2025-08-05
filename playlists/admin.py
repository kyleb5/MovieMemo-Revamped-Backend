from django.contrib import admin
from .models import Playlists, Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['imdb_id', 'added_at']
    search_fields = ['imdb_id']
    readonly_fields = ['added_at']
    ordering = ['-added_at']

@admin.register(Playlists)
class PlaylistsAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'movie_count', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['name', 'description', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'movie_count']
    ordering = ['-created_at']
    filter_horizontal = ['movies']  # Nice UI for many-to-many
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'user')
        }),
        ('Movies', {
            'fields': ('movies',)
        }),
        ('Info', {
            'fields': ('created_at', 'movie_count'),
            'classes': ('collapse',)
        }),
    )
    
    def movie_count(self, obj):
        return obj.movie_count()
    movie_count.short_description = 'Number of Movies'

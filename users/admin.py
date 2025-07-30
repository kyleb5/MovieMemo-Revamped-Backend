from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'uid', 'created_at']
    list_filter = ['created_at']
    search_fields = ['username', 'email', 'uid']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']

from django.db import models
from users.models import CustomUser

class Playlists(models.Model):
    """
    Playlists are made for movies to be added to
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='playlists')
    
    class Meta:
        ordering = ['-created_at']  # Show newest playlists first
        verbose_name_plural = "Playlists"
    
    def __str__(self):
        return f"{self.name} by {self.user.username}"
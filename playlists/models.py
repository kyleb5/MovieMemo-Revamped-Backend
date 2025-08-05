from django.db import models
from users.models import CustomUser

class Movie(models.Model):
    """
    Simple movie model that stores just the IMDb ID
    All other movie data will be fetched from IMDb API when needed
    """
    imdb_id = models.CharField(max_length=20, unique=True)  # IMDb ID (e.g., "tt0111161")
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-added_at']
        verbose_name_plural = "Movies"
    
    def __str__(self):
        return f"Movie {self.imdb_id}"

class Playlists(models.Model):
    """
    Playlists are made for movies to be added to
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='playlists')
    movies = models.ManyToManyField(Movie, blank=True, related_name='playlists')  # Many-to-many relationship
    
    class Meta:
        ordering = ['-created_at']  # Show newest playlists first
        verbose_name_plural = "Playlists"
    
    def __str__(self):
        return f"{self.name} by {self.user.username}"
    
    def movie_count(self):
        """Return the number of movies in this playlist"""
        return self.movies.count()
from rest_framework import serializers
from .models import Playlists, Movie
from users.serializers import PublicUserSerializer

class MovieSerializer(serializers.ModelSerializer):
    """
    Simple serializer for movies with just IMDb ID
    """
    class Meta:
        model = Movie
        fields = ['id', 'imdb_id', 'added_at']
        read_only_fields = ['id', 'added_at']

class PlaylistSerializer(serializers.ModelSerializer):
    """
    Serializer for playlists with public user information and movies
    """
    user = PublicUserSerializer(read_only=True)
    movies = MovieSerializer(many=True, read_only=True)
    movie_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlists
        fields = ['id', 'name', 'description', 'created_at', 'user', 'movies', 'movie_count']
        read_only_fields = ['id', 'created_at', 'user', 'movies', 'movie_count']
    
    def get_movie_count(self, obj):
        return obj.movie_count()

class CreatePlaylistSerializer(serializers.ModelSerializer):
    """
    Serializer for creating playlists (user will be set from request)
    """
    class Meta:
        model = Playlists
        fields = ['name', 'description']
        
    def validate_name(self, value):
        """
        Validate playlist name
        """
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Playlist name cannot be empty")
        if len(value) > 100:
            raise serializers.ValidationError("Playlist name cannot exceed 100 characters")
        return value.strip()

class AddMovieToPlaylistSerializer(serializers.Serializer):
    """
    Serializer for adding a movie to a playlist by IMDb ID (just numbers)
    """
    imdb_id = serializers.CharField(max_length=20)
    
    def validate_imdb_id(self, value):
        """
        Validate IMDb ID - just numbers, no 'tt' prefix needed
        """
        # Remove any whitespace
        value = value.strip()
        
        # Check if it's all digits
        if not value.isdigit():
            raise serializers.ValidationError("IMDb ID must contain only numbers (e.g., '1234567')")
        
        # Check minimum length
        if len(value) < 7:
            raise serializers.ValidationError("IMDb ID must be at least 7 digits")
            
        return value

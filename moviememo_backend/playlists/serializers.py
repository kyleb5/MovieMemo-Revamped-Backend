from rest_framework import serializers
from .models import Playlists
from users.serializers import PublicUserSerializer

class PlaylistSerializer(serializers.ModelSerializer):
    """
    Serializer for playlists with public user information (no email)
    """
    user = PublicUserSerializer(read_only=True)
    
    class Meta:
        model = Playlists
        fields = ['id', 'name', 'description', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']

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

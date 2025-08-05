from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Playlists, Movie
from .serializers import PlaylistSerializer, CreatePlaylistSerializer, AddMovieToPlaylistSerializer
from users.models import CustomUser

@api_view(['POST'])
def create_playlist(request, user_uid):
    """
    Create a new playlist for a specific user
    """
    try:
        user = CustomUser.objects.get(uid=user_uid)
    except CustomUser.DoesNotExist:
        return Response(
            {'message': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = CreatePlaylistSerializer(data=request.data)
    
    if serializer.is_valid():
        playlist = serializer.save(user=user)
        
        # Return full playlist data with public user info
        response_serializer = PlaylistSerializer(playlist)
        return Response(
            {
                'message': 'Playlist created successfully',
                'playlist': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        {
            'message': 'Failed to create playlist',
            'errors': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
def get_user_playlists(request, user_uid):
    """
    Get all playlists for a specific user
    """
    try:
        user = CustomUser.objects.get(uid=user_uid)
    except CustomUser.DoesNotExist:
        return Response(
            {'message': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    playlists = Playlists.objects.filter(user=user)
    serializer = PlaylistSerializer(playlists, many=True)
    
    return Response({
        'playlists': serializer.data,
        'count': playlists.count()
    })

@api_view(['GET'])
def get_all_playlists(request):
    """
    Get all playlists (public view)
    """
    playlists = Playlists.objects.all()
    serializer = PlaylistSerializer(playlists, many=True)
    
    return Response({
        'playlists': serializer.data,
        'count': playlists.count()
    })

@api_view(['GET'])
def get_playlist(request, playlist_id):
    """
    Get a specific playlist by ID
    """
    try:
        playlist = Playlists.objects.get(id=playlist_id)
        serializer = PlaylistSerializer(playlist)
        return Response({
            'playlist': serializer.data
        })
    except Playlists.DoesNotExist:
        return Response(
            {'message': 'Playlist not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['PUT'])
def update_playlist(request, playlist_id):
    """
    Update a playlist (name and/or description)
    """
    try:
        playlist = Playlists.objects.get(id=playlist_id)
    except Playlists.DoesNotExist:
        return Response(
            {'message': 'Playlist not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = CreatePlaylistSerializer(playlist, data=request.data, partial=True)
    
    if serializer.is_valid():
        playlist = serializer.save()
        
        # Return updated playlist with public user info
        response_serializer = PlaylistSerializer(playlist)
        return Response(
            {
                'message': 'Playlist updated successfully',
                'playlist': response_serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    return Response(
        {
            'message': 'Failed to update playlist',
            'errors': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['DELETE'])
def delete_playlist(request, playlist_id):
    """
    Delete a playlist
    """
    try:
        playlist = Playlists.objects.get(id=playlist_id)
        playlist_name = playlist.name
        playlist.delete()
        
        return Response(
            {
                'message': f'Playlist "{playlist_name}" deleted successfully'
            },
            status=status.HTTP_200_OK
        )
    except Playlists.DoesNotExist:
        return Response(
            {'message': 'Playlist not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
def add_movie_to_playlist(request, playlist_id):
    """
    Add a movie to a playlist by IMDb ID
    """
    try:
        playlist = Playlists.objects.get(id=playlist_id)
    except Playlists.DoesNotExist:
        return Response(
            {'message': 'Playlist not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = AddMovieToPlaylistSerializer(data=request.data)
    
    if serializer.is_valid():
        imdb_id = serializer.validated_data['imdb_id']
        
        # Get or create the movie
        movie, created = Movie.objects.get_or_create(imdb_id=imdb_id)
        
        # Check if movie is already in playlist
        if playlist.movies.filter(id=movie.id).exists():
            return Response(
                {'message': f'Movie {imdb_id} is already in this playlist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add movie to playlist
        playlist.movies.add(movie)
        
        # Return updated playlist
        response_serializer = PlaylistSerializer(playlist)
        return Response(
            {
                'message': f'Movie {imdb_id} added to playlist successfully',
                'playlist': response_serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    return Response(
        {
            'message': 'Failed to add movie to playlist',
            'errors': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['DELETE'])
def remove_movie_from_playlist(request, playlist_id, imdb_id):
    """
    Remove a movie from a playlist by IMDb ID
    """
    try:
        playlist = Playlists.objects.get(id=playlist_id)
    except Playlists.DoesNotExist:
        return Response(
            {'message': 'Playlist not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        movie = Movie.objects.get(imdb_id=imdb_id)
    except Movie.DoesNotExist:
        return Response(
            {'message': 'Movie not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if movie is in playlist
    if not playlist.movies.filter(id=movie.id).exists():
        return Response(
            {'message': f'Movie {imdb_id} is not in this playlist'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Remove movie from playlist
    playlist.movies.remove(movie)
    
    # Return updated playlist
    response_serializer = PlaylistSerializer(playlist)
    return Response(
        {
            'message': f'Movie {imdb_id} removed from playlist successfully',
            'playlist': response_serializer.data
        },
        status=status.HTTP_200_OK
    )

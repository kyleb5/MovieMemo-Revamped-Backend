from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Playlists
from .serializers import PlaylistSerializer, CreatePlaylistSerializer
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

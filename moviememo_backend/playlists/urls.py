from django.urls import path
from . import views

urlpatterns = [
    # POST /api/playlists/create/<user_uid>/
    # Create a new playlist for a user
    path('create/<str:user_uid>/', views.create_playlist, name='create_playlist'),
    
    # GET /api/playlists/user/<user_uid>/
    # Get all playlists for a specific user
    path('user/<str:user_uid>/', views.get_user_playlists, name='get_user_playlists'),
    
    # GET /api/playlists/all/
    # Get all playlists (public view)
    path('all/', views.get_all_playlists, name='get_all_playlists'),
    
    # GET /api/playlists/<playlist_id>/
    # Get a specific playlist
    path('<int:playlist_id>/', views.get_playlist, name='get_playlist'),
    
    # PUT /api/playlists/<playlist_id>/update/
    # Update a playlist
    path('<int:playlist_id>/update/', views.update_playlist, name='update_playlist'),
    
    # DELETE /api/playlists/<playlist_id>/delete/
    # Delete a playlist
    path('<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
]

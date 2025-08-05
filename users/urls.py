from django.urls import path
from . import views

urlpatterns = [
    # POST /api/users/create/
    # Create a new user
    path('create/', views.create_user, name='create_user'),
    
    # GET /api/users/all/
    # Get all users (public data only)
    path('all/', views.get_all_users, name='get_all_users'),
    
    # GET /api/users/check/<uid>/
    # Check if a user exists by UID (returns true/false)
    path('check/<str:uid>/', views.check_user_exists, name='check_user_exists'),
    
    # GET /api/users/check/username/<username>/
    # Check if a user exists by username (returns true/false)
    path('check/username/<str:username>/', views.check_user_username_exists, name='check_user_username_exists'),
    
    # PUT /api/users/<uid>/profile-picture/
    # Upload or update user's profile picture
    path('<str:username>/profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    
    # GET /api/users/username/<username>/
    # Get a user by username
    path('username/<str:username>/', views.get_username_user, name='get_username_user'),
    
    # GET /api/users/<uid>/
    # Get a user by UID
    path('<str:uid>/', views.get_public_user, name='get_public_user'),
    
    # PUT /api/users/<uid>/change-username/
    # Change current username
    path('<str:uid>/change_username/', views.change_username, name='change_username'),
]

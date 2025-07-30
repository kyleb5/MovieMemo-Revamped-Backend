from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user, name='create_user'),
    path('check/<str:uid>/', views.check_user_exists, name='check_user_exists'),
    path('check/username/<str:username>/', views.check_user_username_exists, name='check_user_username_exists'),
    path('username/<str:username>/', views.get_username_user, name='get_username_user'),
    path('<str:uid>/', views.get_public_user, name='get_public_user'),
]

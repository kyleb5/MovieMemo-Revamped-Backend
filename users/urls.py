from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user, name='create_user'),
    path('check/<str:uid>/', views.check_user_exists, name='check_user_exists'),
    path('<str:uid>/', views.get_public_user, name='get_public_user'),
]

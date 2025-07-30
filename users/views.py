from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, PublicUserSerializer


@api_view(['POST'])
def create_user(request):
    """
    Create a new custom user with email and uid.
    """
    serializer = CustomUserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        # Return public data without email for security
        return Response(
            {
                'message': 'User created successfully',
                'user': PublicUserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        {
            'message': 'Failed to create user',
            'errors': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def get_public_user(request, uid):
    """
    Get a specific user's public information by ID.
    Returns only public data (no email).
    """
    try:
        user = CustomUser.objects.get(uid=uid)
        serializer = PublicUserSerializer(user)
        return Response({
            'user': serializer.data
        })
    except CustomUser.DoesNotExist:
        return Response(
            {
                'message': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def get_username_user(request, username):
    """
    Get a specific user publicly based off there username
    """
    try:
        user = CustomUser.objects.get(username=username)
        serializer = PublicUserSerializer(user)
        return Response({
            'user': serializer.data
        })
    except CustomUser.DoesNotExist:
        return Response(
            {
                'message': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def check_user_exists(request, uid):
    """
    Check if a user exists by UID.
    Returns true or false.
    """
    exists = CustomUser.objects.filter(uid=uid).exists()
    return Response({
        'exists': exists,
        'uid': uid
    })

@api_view(['GET'])
def check_user_username_exists(request, username):
    """
    Check if a user exists by username
    Returns true or false.
    """
    exists = CustomUser.objects.filter(username=username).exists()
    return Response({
        'exists': exists,
        'username': username
    })

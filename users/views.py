from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, PublicUserSerializer
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Register HEIF support for PIL
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass  # HEIF support not available


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


@api_view(['GET'])
def get_all_users(request):
    """
    Get all users (public data only - no emails)
    """
    users = CustomUser.objects.all()
    serializer = PublicUserSerializer(users, many=True)
    return Response({
        'users': serializer.data,
        'count': users.count()
    })


@api_view(['PUT'])
def upload_profile_picture(request, username):
    """
    Upload or update a user's profile picture.
    Automatically converts any uploaded image to WebP format.
    Accepts multipart/form-data with 'profile_picture' field.
    """
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response(
            {'message': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if 'profile_picture' not in request.FILES:
        return Response(
            {'message': 'No profile picture file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check that only one file is being uploaded
    if len(request.FILES) > 1:
        return Response(
            {'message': 'Only one profile picture file allowed per upload'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check that only one profile_picture file is provided
    profile_picture_files = request.FILES.getlist('profile_picture')
    if len(profile_picture_files) > 1:
        return Response(
            {'message': 'Only one profile picture file allowed per upload'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate the uploaded file before making any changes
    from django.core.exceptions import ValidationError
    temp_file = request.FILES['profile_picture']
    
    try:
        from .models import validate_image_file_extension, validate_file_size
        validate_image_file_extension(temp_file)
        validate_file_size(temp_file)
    except ValidationError as e:
        return Response(
            {
                'message': 'Failed to upload profile picture',
                'error': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Convert image to WebP format with consistent sizing
    try:
        # Open and process the image
        image = Image.open(temp_file)
        
        # Define standard profile picture size
        PROFILE_PICTURE_SIZE = (200, 200)  # 400x400 pixels
        
        # Convert to RGB if necessary (WebP works best with RGB)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGBA")
        else:
            image = image.convert("RGB")
        
        # Resize image to standard size (400x400)
        image = image.resize(PROFILE_PICTURE_SIZE, Image.Resampling.LANCZOS)
            
        # Create a BytesIO buffer to save the WebP image
        buffer = BytesIO()
        image.save(buffer, format="WEBP", quality=85, optimize=True)
        buffer.seek(0)
        
        # Create a ContentFile with the WebP data
        webp_file = ContentFile(buffer.read(), name=f"{user.username}.webp")
        
    except Exception as e:
        return Response(
            {
                'message': 'Failed to convert image to WebP',
                'error': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Delete old profile picture if it exists
    if user.profile_picture:
        user.profile_picture.delete(save=False)
    
    # Save the WebP converted image
    user.profile_picture = webp_file
    
    try:
        user.save()
        
        return Response(
            {
                'message': 'Profile picture uploaded and converted to WebP successfully',
                'user': PublicUserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {
                'message': 'Failed to save profile picture',
                'error': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

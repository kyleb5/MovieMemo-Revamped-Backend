from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import os
import time


def validate_image_file_extension(value):
    """
    Validate that the uploaded file is an image
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.heif']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Only image files are allowed (jpg, jpeg, png, gif, bmp, webp, heic, heif)')


def validate_file_size(value):
    """
    Validate that the uploaded file is not larger than 10MB
    """
    filesize = value.size
    max_size = 10 * 1024 * 1024  # 10MB in bytes
    if filesize > max_size:
        raise ValidationError(f'File size cannot exceed 10MB. Current file size: {filesize / (1024*1024):.1f}MB')


def profile_picture_upload_path(instance, filename):
    """
    Generate upload path using the user's username with webp extension
    All profile pictures are converted to webp format
    Includes timestamp for cache busting
    """
    # Add timestamp to force cache busting
    timestamp = int(time.time())
    new_filename = f"{instance.username}_{timestamp}.webp"
    return f"profile_pictures/{new_filename}"


class CustomUser(models.Model):
    """
    Custom user model that stores email and uid.
    This is separate from Django's built-in User model.
    """
    email = models.EmailField(unique=True)
    uid = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=16, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_username_change = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=profile_picture_upload_path,
        validators=[validate_image_file_extension, validate_file_size],
        blank=True,
        null=True
    )
    
    class Meta:
        db_table = 'custom_users'
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
    
    def __str__(self):
        return f"{self.email} ({self.uid})"

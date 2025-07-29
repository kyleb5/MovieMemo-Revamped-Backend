from django.db import models


class CustomUser(models.Model):
    """
    Custom user model that stores email and uid.
    This is separate from Django's built-in User model.
    """
    email = models.EmailField(unique=True)
    uid = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=16, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'custom_users'
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
    
    def __str__(self):
        return f"{self.email} ({self.uid})"

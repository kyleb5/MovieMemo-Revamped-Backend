from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'uid', 'username', 'created_at', 'profile_picture']
        read_only_fields = ['id', 'created_at']
    
    def get_profile_picture(self, obj):
        """Return the profile picture URL or default if none uploaded"""
        if obj.profile_picture and obj.profile_picture.name:
            return obj.profile_picture.url
        return "https://cdn.kyleb.dev/pfp/defaultpfp.png"
    
    def validate_email(self, value):
        """
        Check that the email is valid and not already in use.
        """
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_uid(self, value):
        """
        Check that the uid is not already in use.
        """
        if CustomUser.objects.filter(uid=value).exists():
            raise serializers.ValidationError("A user with this UID already exists.")
        return value

    def validate_username(self, value):
        """
        Check if the username is already in use
        """
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user wit the same username already exists!!")
        return value


class PublicUserSerializer(serializers.ModelSerializer):
    """
    Serializer for public user data - excludes email for privacy
    """
    profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['uid', 'username', 'created_at', 'profile_picture']
        read_only_fields = ['id', 'created_at']
    
    def get_profile_picture(self, obj):
        """Return the profile picture URL or default if none uploaded"""
        if obj.profile_picture and obj.profile_picture.name:
            return obj.profile_picture.url
        return "https://cdn.kyleb.dev/pfp/defaultpfp.png"

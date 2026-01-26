from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'balance', 'is_staff', 'avatar_url')
        read_only_fields = ('balance', 'is_staff', 'avatar_url')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    registration_cookie = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'registration_cookie')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        import random
        # Remove fields that are not part of User model creation directly if needed
        cookie = validated_data.pop('registration_cookie', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.registration_cookie = cookie
        # Assign random avatar
        avatars = [
            "https://api.dicebear.com/7.x/avataaars/svg?seed=Felix",
            "https://api.dicebear.com/7.x/avataaars/svg?seed=Aneka",
            "https://api.dicebear.com/7.x/avataaars/svg?seed=Zack",
            "https://api.dicebear.com/7.x/avataaars/svg?seed=Midnight",
            "https://api.dicebear.com/7.x/avataaars/svg?seed=Lily",
        ]
        user.avatar_url = f"https://api.dicebear.com/7.x/avataaars/svg?seed={user.username}"
        user.save()
        return user

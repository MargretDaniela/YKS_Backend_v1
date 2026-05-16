
# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class RegisterSerializer(serializers.ModelSerializer):
#     # CHANGE: Accept 'full_name' instead of 'first_name'/'last_name'
#     full_name        = serializers.CharField(write_only=True)
#     password         = serializers.CharField(write_only=True, min_length=6)
#     confirm_password = serializers.CharField(write_only=True)

#     class Meta:
#         model  = User
#         # CHANGE: Updated fields list
#         fields = ["full_name", "email", "password", "confirm_password"]

#     def validate(self, data):
#         if data["password"] != data["confirm_password"]:
#             raise serializers.ValidationError("Passwords do not match.")
#         return data

#     def validate_email(self, value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("This email is already registered.")
#         return value

#     def create(self, validated_data):
#         validated_data.pop("confirm_password")
        
#         # CHANGE: Directly use full_name
#         full_name = validated_data.pop("full_name")
        
#         return User.objects.create_user(
#             email=validated_data["email"],
#             password=validated_data["password"],
#             full_name=full_name,
#             role="STUDENT",
#         )


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model  = User
#         fields = ["id", "full_name", "email", "role", "is_active", "date_joined"]

# C:\Users\Admin\Desktop\TheYKSApp\accounts\serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


# ======================================================================
#  RegisterSerializer — For user registration
# ======================================================================
class RegisterSerializer(serializers.ModelSerializer):
    full_name        = serializers.CharField(write_only=True)
    password         = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ["full_name", "email", "password", "confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        full_name = validated_data.pop("full_name")
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=full_name,
            role="STUDENT",
        )


# ======================================================================
#  UserSerializer — For user data responses
# ======================================================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ["id", "full_name", "email", "role", "is_active", "date_joined"]
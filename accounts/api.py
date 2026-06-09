
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate, get_user_model
# from django.core.cache import cache
# from .serializers import RegisterSerializer, UserSerializer
# from .otp import send_otp_email, send_password_reset_email, generate_otp
# from .models import OTPCode
# from django.utils import timezone
# from datetime import timedelta

# User = get_user_model()


# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         "refresh": str(refresh),
#         "access":  str(refresh.access_token),
#     }


# # ── EXISTING ENDPOINTS ────────────────────────────────────────────────

# @api_view(["POST"])
# @permission_classes([AllowAny])
# def register_api(request):
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         user   = serializer.save()
#         tokens = get_tokens_for_user(user)
#         try:
#             send_otp_email(user)
#         except Exception as e:
#             print(f"Email error: {e}")
#         return Response({
#             "success": True,
#             "message": "Account created. Check your email for the verification code.",
#             "tokens":  tokens,
#             "user":    UserSerializer(user).data,
#         }, status=status.HTTP_201_CREATED)

#     return Response({
#         "success": False,
#         "errors":  serializer.errors,
#     }, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login_api(request):
#     email    = request.data.get("email", "").strip()
#     password = request.data.get("password", "")

#     if not email or not password:
#         return Response({
#             "success": False,
#             "error":   "Email and password are required.",
#         }, status=status.HTTP_400_BAD_REQUEST)

#     user = authenticate(request, email=email, password=password)

#     if user is None:
#         return Response({
#             "success": False,
#             "error":   "Invalid email or password.",
#         }, status=status.HTTP_401_UNAUTHORIZED)

#     if not user.is_active:
#         return Response({
#             "success": False,
#             "error":   "Your account has been deactivated.",
#         }, status=status.HTTP_403_FORBIDDEN)

#     tokens = get_tokens_for_user(user)
#     return Response({
#         "success": True,
#         "message": "Login successful.",
#         "tokens":  tokens,
#         "user":    UserSerializer(user).data,
#     }, status=status.HTTP_200_OK)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def verify_otp_api(request):
#     email = request.data.get("email", "").strip()
#     code  = request.data.get("code", "").strip()

#     if not email or not code:
#         return Response({
#             "success": False,
#             "error":   "Email and code are required.",
#         }, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return Response({
#             "success": False,
#             "error":   "User not found.",
#         }, status=status.HTTP_404_NOT_FOUND)

#     otp = user.otp_codes.filter(code=code, is_used=False).last()

#     if not otp or not otp.is_valid():
#         return Response({
#             "success": False,
#             "error":   "Invalid or expired code. Please request a new one.",
#         }, status=status.HTTP_400_BAD_REQUEST)

#     otp.is_used   = True
#     otp.save()
#     user.is_verified = True
#     user.save()

#     return Response({
#         "success": True,
#         "message": "Email verified successfully!",
#     }, status=status.HTTP_200_OK)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def resend_otp_api(request):
#     email = request.data.get("email", "").strip()

#     if not email:
#         return Response({"success": False, "error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return Response({"success": False, "error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

#     try:
#         send_otp_email(user)
#     except Exception as e:
#         return Response({"success": False, "error": "Failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     return Response({"success": True, "message": "New code sent to your email."})


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def refresh_token_api(request):
#     refresh_token = request.data.get("refresh")
#     if not refresh_token:
#         return Response({"error": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
#     try:
#         refresh = RefreshToken(refresh_token)
#         return Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)
#     except Exception:
#         return Response({"error": "Invalid or expired refresh token."}, status=status.HTTP_401_UNAUTHORIZED)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def me_api(request):
#     user = request.user
#     return Response({
#         'success': True,
#         'user': {
#             'id':        user.pk,
#             'email':     user.email,
#             'full_name': getattr(user, 'full_name', '') or '',
#             'role':      getattr(user, 'role', 'STUDENT') or 'STUDENT',
#         }
#     })


# # ── FORGOT PASSWORD ENDPOINTS ─────────────────────────────────────────

# @api_view(["POST"])
# @permission_classes([AllowAny])
# def forgot_password_api(request):
#     """
#     Step 1: User submits their email.
#     We send a 6-digit OTP to that email for password reset.
#     We never confirm if the email exists (security best practice).
#     """
#     email = request.data.get("email", "").strip()

#     if not email:
#         return Response({
#             "success": False,
#             "error":   "Email is required.",
#         }, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.get(email=email)

#         # Generate and save OTP
#         OTPCode.objects.filter(user=user).delete()
#         code       = generate_otp()
#         expires_at = timezone.now() + timedelta(minutes=10)
#         OTPCode.objects.create(user=user, code=code, expires_at=expires_at)

#         # Send reset email
#         send_password_reset_email(user, code)

#     except User.DoesNotExist:
#         # We still return success to avoid email enumeration
#         pass
#     except Exception as e:
#         print(f"Password reset email error: {e}")
#         return Response({
#             "success": False,
#             "error":   "Failed to send reset email. Please try again.",
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     return Response({
#         "success": True,
#         "message": "If that email exists, a reset code has been sent.",
#     }, status=status.HTTP_200_OK)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def verify_reset_otp_api(request):
#     """
#     Step 2: User submits email + OTP code.
#     Returns a short-lived reset token stored in cache.
#     Frontend uses this token in the final reset step.
#     """
#     email = request.data.get("email", "").strip()
#     code  = request.data.get("code",  "").strip()

#     if not email or not code:
#         return Response({
#             "success": False,
#             "error":   "Email and code are required.",
#         }, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return Response({
#             "success": False,
#             "error":   "Invalid code or email.",
#         }, status=status.HTTP_400_BAD_REQUEST)

#     otp = user.otp_codes.filter(code=code, is_used=False).last()

#     if not otp or not otp.is_valid():
#         return Response({
#             "success": False,
#             "error":   "Invalid or expired code. Please request a new one.",
#         }, status=status.HTTP_400_BAD_REQUEST)

#     # Mark OTP as used
#     otp.is_used = True
#     otp.save()

#     # Store a reset token in cache (valid for 15 minutes)
#     import secrets
#     reset_token = secrets.token_urlsafe(32)
#     cache_key   = f"password_reset_{reset_token}"
#     cache.set(cache_key, user.pk, timeout=60 * 15)

#     return Response({
#         "success":     True,
#         "message":     "Code verified. You may now reset your password.",
#         "reset_token": reset_token,
#     }, status=status.HTTP_200_OK)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def reset_password_api(request):
#     """
#     Step 3: User submits reset_token + new password.
#     Token is validated from cache, then deleted after use.
#     """
#     reset_token      = request.data.get("reset_token", "").strip()
#     new_password     = request.data.get("new_password", "")
#     confirm_password = request.data.get("confirm_password", "")

#     if not reset_token or not new_password or not confirm_password:
#         return Response({
#             "success": False,
#             "error":   "reset_token, new_password and confirm_password are all required.",
#         }, status=status.HTTP_400_BAD_REQUEST)

#     if new_password != confirm_password:
#         return Response({
#             "success": False,
#             "error":   "Passwords do not match.",
#         }, status=status.HTTP_400_BAD_REQUEST)

#     if len(new_password) < 8:
#         return Response({
#             "success": False,
#             "error":   "Password must be at least 8 characters.",
#         }, status=status.HTTP_400_BAD_REQUEST)

#     # Look up token in cache
#     cache_key = f"password_reset_{reset_token}"
#     user_pk   = cache.get(cache_key)

#     if not user_pk:
#         return Response({
#             "success": False,
#             "error":   "Reset token is invalid or has expired. Please start over.",
#         }, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.get(pk=user_pk)
#     except User.DoesNotExist:
#         return Response({
#             "success": False,
#             "error":   "User not found.",
#         }, status=status.HTTP_404_NOT_FOUND)

# # Set new password
#     user.set_password(new_password)
#     user.save(update_fields=["password"])

#     # Re-fetch from DB to clear any cached state
#     user.refresh_from_db()

#     # Delete token from cache so it can't be reused
#     cache.delete(cache_key)

#     return Response({
#         "success": True,
#         "message": "Password reset successfully. You can now log in.",
#     }, status=status.HTTP_200_OK)

# C:\Users\Admin\Desktop\TheYKSApp\accounts\api.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.core.cache import cache
from .serializers import RegisterSerializer, UserSerializer
from .otp import send_otp_email, send_password_reset_email, generate_otp
from .models import OTPCode
from django.utils import timezone
from datetime import timedelta
import secrets

User = get_user_model()


def get_tokens_for_user(user):
    """Generate JWT tokens for a user"""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# ======================================================================
#  🔐 REGISTER - Fixed to accept full_name
# ======================================================================
@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    """Register a new user with full_name, email, password"""
    
    # ✅ Accept both 'full_name' OR 'first_name' + 'last_name' for flexibility
    full_name = request.data.get("full_name", "").strip()
    first_name = request.data.get("first_name", "").strip()
    last_name = request.data.get("last_name", "").strip()
    
    # If full_name not provided, combine first + last
    if not full_name and first_name and last_name:
        full_name = f"{first_name} {last_name}".strip()
    
    email = request.data.get("email", "").strip().lower()
    password = request.data.get("password", "")
    confirm_password = request.data.get("confirm_password", "")
    
    # Validation
    if not full_name:
        return Response({
            "success": False,
            "error": "Full name is required.",
            "errors": {"full_name": ["This field is required."]}
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not email or "@" not in email:
        return Response({
            "success": False,
            "error": "Valid email is required.",
            "errors": {"email": ["Enter a valid email address."]}
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if len(password) < 6:
        return Response({
            "success": False,
            "error": "Password must be at least 6 characters.",
            "errors": {"password": ["This password is too short."]}
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if password != confirm_password:
        return Response({
            "success": False,
            "error": "Passwords do not match.",
            "errors": {"confirm_password": ["Passwords do not match."]}
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if email already exists
    if User.objects.filter(email=email).exists():
        return Response({
            "success": False,
            "error": "An account with this email already exists.",
            "errors": {"email": ["This email is already registered."]}
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            role="STUDENT",  # Default role
            is_verified=False,
        )
        
        # Generate tokens
        tokens = get_tokens_for_user(user)
        
        # Send OTP email (non-blocking)
        try:
            send_otp_email(user)
        except Exception as e:
            print(f"⚠️ OTP email failed: {e}")
            # Don't fail registration if email fails
        
        return Response({
            "success": True,
            "message": "Account created! Check your email for verification code.",
            "tokens": tokens,
            "user": UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return Response({
            "success": False,
            "error": "Registration failed. Please try again.",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ======================================================================
#  🔐 LOGIN
# ======================================================================
@api_view(["POST"])
@permission_classes([AllowAny])
def login_api(request):
    """Handle user login with email + password"""
    email = request.data.get("email", "").strip().lower()
    password = request.data.get("password", "")

    if not email or not password:
        return Response({
            "success": False,
            "error": "Email and password are required.",
        }, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate (Django's authenticate uses username field, so we pass email)
    user = authenticate(request, username=email, password=password)

    if user is None:
        return Response({
            "success": False,
            "error": "Invalid email or password.",
        }, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({
            "success": False,
            "error": "Your account has been deactivated. Contact support.",
        }, status=status.HTTP_403_FORBIDDEN)

    tokens = get_tokens_for_user(user)
    
    return Response({
        "success": True,
        "message": "Login successful.",
        "tokens": tokens,
        "user": UserSerializer(user).data,
    }, status=status.HTTP_200_OK)


# ======================================================================
#  🔑 VERIFY OTP
# ======================================================================
@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp_api(request):
    """Verify email OTP after registration"""
    email = request.data.get("email", "").strip().lower()
    code = request.data.get("code", "").strip()

    if not email or not code:
        return Response({
            "success": False,
            "error": "Email and verification code are required.",
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            "success": False,
            "error": "User not found.",
        }, status=status.HTTP_404_NOT_FOUND)

    # Find valid, unused OTP
    otp = user.otp_codes.filter(code=code, is_used=False).first()

    if not otp or not otp.is_valid():
        return Response({
            "success": False,
            "error": "Invalid or expired code. Please request a new one.",
        }, status=status.HTTP_400_BAD_REQUEST)

    # Mark OTP as used and verify user
    otp.is_used = True
    otp.save()
    user.is_verified = True
    user.save(update_fields=['is_verified'])

    return Response({
        "success": True,
        "message": "Email verified successfully! You can now log in.",
    }, status=status.HTTP_200_OK)


# ======================================================================
#  📧 RESEND OTP
# ======================================================================
@api_view(["POST"])
@permission_classes([AllowAny])
def resend_otp_api(request):
    """Resend OTP to user's email"""
    email = request.data.get("email", "").strip().lower()

    if not email:
        return Response({"success": False, "error": "Email is required."}, 
                       status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Return success anyway to prevent email enumeration
        return Response({"success": True, "message": "If that email exists, a new code was sent."})

    try:
        # Delete old OTPs and send new one
        user.otp_codes.filter(is_used=False).delete()
        send_otp_email(user)
    except Exception as e:
        print(f"⚠️ Resend OTP error: {e}")
        return Response({"success": False, "error": "Failed to send email. Try again."}, 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"success": True, "message": "New verification code sent to your email."})


# ======================================================================
#  🔄 REFRESH TOKEN
# ======================================================================
@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token_api(request):
    """Refresh access token using refresh token"""
    refresh_token = request.data.get("refresh")
    
    if not refresh_token:
        return Response({"error": "Refresh token required."}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        refresh = RefreshToken(refresh_token)
        return Response({
            "success": True,
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"❌ Token refresh error: {e}")
        return Response({"error": "Invalid or expired refresh token."}, 
                       status=status.HTTP_401_UNAUTHORIZED)


# ======================================================================
#  👤 GET CURRENT USER
# ======================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_api(request):
    """Get current authenticated user's profile"""
    user = request.user
    return Response({
        'success': True,
        'user': {
            'id': user.pk,
            'email': user.email,
            'full_name': getattr(user, 'full_name', '') or user.email,
            'role': getattr(user, 'role', 'STUDENT'),
            'is_verified': getattr(user, 'is_verified', False),
            'date_joined': str(user.date_joined) if hasattr(user, 'date_joined') else None,
        }
    })


# ======================================================================
#  🔐 FORGOT PASSWORD - Step 1: Request Reset Code
# ======================================================================
@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password_api(request):
    """
    Step 1: User submits email → send password reset OTP.
    Security: Never confirm if email exists (prevent enumeration).
    """
    email = request.data.get("email", "").strip().lower()

    if not email:
        return Response({
            "success": False,
            "error": "Email is required.",
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)

        # Delete old unused OTPs and create a new one
        OTPCode.objects.filter(user=user, is_used=False).delete()
        code = generate_otp()
        expires_at = timezone.now() + timedelta(minutes=10)

        # ✅ FIX: removed purpose='password_reset' — field doesn't exist on OTPCode model
        OTPCode.objects.create(user=user, code=code, expires_at=expires_at)

        # Send reset email (non-blocking)
        try:
            send_password_reset_email(user, code)
        except Exception as e:
            print(f"⚠️ Reset email failed: {e}")

    except User.DoesNotExist:
        # Return success anyway to prevent email enumeration
        pass
    except Exception as e:
        print(f"❌ Forgot password error: {e}")
        return Response({
            "success": False,
            "error": "Failed to process request. Please try again.",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "success": True,
        "message": "If that email exists, a reset code has been sent.",
    }, status=status.HTTP_200_OK)


# ======================================================================
#  🔐 VERIFY RESET OTP - Step 2
# ======================================================================
@api_view(["POST"])
@permission_classes([AllowAny])
def verify_reset_otp_api(request):
    """
    Step 2: Verify OTP and return short-lived reset token.
    """
    email = request.data.get("email", "").strip().lower()
    code = request.data.get("code", "").strip()

    if not email or not code:
        return Response({
            "success": False,
            "error": "Email and code are required.",
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            "success": False,
            "error": "Invalid code or email.",
        }, status=status.HTTP_400_BAD_REQUEST)

    # ✅ FIX: removed purpose='password_reset' filter — field doesn't exist on OTPCode model
    otp = user.otp_codes.filter(
        code=code,
        is_used=False,
    ).first()

    if not otp or not otp.is_valid():
        return Response({
            "success": False,
            "error": "Invalid or expired code. Please request a new one.",
        }, status=status.HTTP_400_BAD_REQUEST)

    # Mark OTP as used
    otp.is_used = True
    otp.save()

    # Generate secure reset token (stored in cache, 15 min expiry)
    reset_token = secrets.token_urlsafe(32)
    cache_key = f"password_reset_{reset_token}"
    cache.set(cache_key, user.pk, timeout=60 * 15)

    return Response({
        "success": True,
        "message": "Code verified. You may now reset your password.",
        "reset_token": reset_token,
    }, status=status.HTTP_200_OK)


# ======================================================================
#  🔐 RESET PASSWORD - Step 3: Final Password Change
# ======================================================================
@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_api(request):
    """
    Step 3: Use reset_token to set new password.
    Token is consumed after use (one-time).
    """
    reset_token = request.data.get("reset_token", "").strip()
    new_password = request.data.get("new_password", "")
    confirm_password = request.data.get("confirm_password", "")

    if not reset_token or not new_password or not confirm_password:
        return Response({
            "success": False,
            "error": "reset_token, new_password and confirm_password are all required.",
        }, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response({
            "success": False,
            "error": "Passwords do not match.",
        }, status=status.HTTP_400_BAD_REQUEST)

    if len(new_password) < 8:
        return Response({
            "success": False,
            "error": "Password must be at least 8 characters.",
        }, status=status.HTTP_400_BAD_REQUEST)

    # Validate reset token from cache
    cache_key = f"password_reset_{reset_token}"
    user_pk = cache.get(cache_key)

    if not user_pk:
        return Response({
            "success": False,
            "error": "Reset token is invalid or has expired. Please start over.",
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        cache.delete(cache_key)  # Clean up
        return Response({
            "success": False,
            "error": "User not found.",
        }, status=status.HTTP_404_NOT_FOUND)

    # Set new password
    user.set_password(new_password)
    user.save(update_fields=["password"])
    user.refresh_from_db()

    # Delete used token
    cache.delete(cache_key)

    return Response({
        "success": True,
        "message": "Password reset successfully. You can now log in.",
    }, status=status.HTTP_200_OK)
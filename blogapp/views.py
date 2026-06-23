from django.shortcuts import render, get_object_or_404
from .models import Blog, NewsletterSubscription
from blogapp.serializers import UpdateuserProfileSerializer, UserRegistrationSerializer, BlogSerializer, UserInfoSerializer, SimpleAuthorSerializer, NewsletterSubscriptionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail


class BlogListPagination(PageNumberPagination):
    page_size= 3


# Create your views here.
@api_view(["GET"])
@permission_classes([AllowAny])
def blog_list(request):
    blogs = Blog.objects.all()
    paginator = BlogListPagination()
    paginated_blogs = paginator.paginate_queryset(blogs, request)
    serializer = BlogSerializer(paginated_blogs, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    serializer = BlogSerializer(blog)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    serializer = UpdateuserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_blog(request):
    user = request.user
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updated_blog(request, pk):
    user = request.user
    blog = Blog.objects.get(id=pk)
    if(blog.author != user):
        return Response({"error": "You are not the author of this blog"}, status=status.HTTP_403_FORBIDDEN)
    serializer = BlogSerializer(blog, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_blog(request,pk):
    blog = Blog.objects.get(id=pk)
    user = request.user
    if blog.author != user:
        return Response({"error": "You are not the author of this blog"}, status=status.HTTP_403_FORBIDDEN)
    blog.delete()
    return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_username(request):
    user = request.user
    username = user.username
    return Response({"username": username})


@api_view(['GET'])
def get_userinfo(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    serializer = UserInfoSerializer(user)
    return Response(serializer.data)


@api_view(["GET"])
def get_user(request, email):
    User = get_user_model()
    try:
        existing_user = User.objects.get(email=email)
        serializer = SimpleAuthorSerializer(existing_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    User = get_user_model()
    user = User.objects.filter(email=email).first()
    
    if user:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:5173/reset-password?uid={uid}&token={token}"
        
        subject = "Password Reset Request"
        message = (
            f"Hello {user.username},\n\n"
            f"We received a password reset request for your account.\n"
            f"Please click the link below to set a new password:\n\n"
            f"{reset_link}\n\n"
            f"If you did not request this, please ignore this email.\n"
        )
        
        try:
            send_mail(
                subject,
                message,
                "support@devfolio.com",
                [email],
                fail_silently=False,
            )
        except Exception:
            # Don't raise a 500 if email sending fails (e.g. SMTP not configured)
            pass
        
    return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    uid = request.data.get("uid")
    token = request.data.get("token")
    password = request.data.get("password")
    
    if not uid or not token or not password:
        return Response({"error": "uid, token, and password are all required."}, status=status.HTTP_400_BAD_REQUEST)
        
    User = get_user_model()
    try:
        uid_decoded = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid_decoded)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user and default_token_generator.check_token(user, token):
        user.set_password(password)
        user.save()
        return Response({"message": "Password has been successfully reset!"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid or expired password reset link."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def subscribe_newsletter(request):
    serializer = NewsletterSubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        subscription = serializer.save()

        # Send a confirmation email to the subscriber
        subject = "Welcome to DevFolio Newsletter! 🎉"
        message = (
            f"Hi there,\n\n"
            f"Thank you for subscribing to the DevFolio Weekly Newsletter!\n\n"
            f"You'll now receive the latest blog articles, tech insights, and exclusive offers "
            f"straight to your inbox at {subscription.email}.\n\n"
            f"Stay tuned for great content!\n\n"
            f"— The DevFolio Team"
        )
        try:
            send_mail(
                subject,
                message,
                "support@devfolio.com",
                [subscription.email],
                fail_silently=True,
            )
        except Exception:
            pass  # Don't block subscription if email fails

        return Response({"message": "Subscribed successfully! Check your email for confirmation."}, status=status.HTTP_201_CREATED)
    
    # Custom message if the email is already subscribed
    if "email" in serializer.errors and any(
        getattr(err, "code", None) == "unique" or "unique" in str(err) or "exists" in str(err).lower()
        for err in serializer.errors["email"]
    ):
        return Response({"error": "This email is already subscribed."}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




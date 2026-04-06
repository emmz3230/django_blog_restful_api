from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Blog 


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "username", "first_name", "last_name", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user_model = get_user_model()

        new_user = user_model.objects.create(
            email=validated_data.get("email", ""),
            username=validated_data.get("username", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        new_user.set_password(validated_data["password"])
        new_user.save()
        return new_user
    

class SimpleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name"]


class BlogSerializer(serializers.ModelSerializer):
    author = SimpleAuthorSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ["id", "title", "slug", "author", "category", "content", "featured_image", "published_date", "created_at", "updated_at", "is_draft"] 
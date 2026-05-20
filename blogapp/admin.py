from django.contrib import admin
from django.contrib.auth.admin  import UserAdmin
from .models import CustomUser, Blog
from django.utils.translation import gettext_lazy as _


# Register your models here.


class CustomUserAdmin(UserAdmin):
        list_display = ("username", "first_name", "last_name", "email", "job_title", "profile_picture", "profile_picture_url")
        fieldsets = (
            (None, {"fields": ("username", "email", "password")}),
            (_("Personal info"), {"fields": ("first_name", "last_name", "job_title", "bio", "profile_picture", "profile_picture_url","facebook", "youtube", "instagram", "twitter", "linkedin")}),
            (_("Permissions"), {"fields": ("is_active","is_staff","is_superuser","groups","user_permissions")}),
            (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        )

        add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('bio', 'profile_picture', 'job_title', 'facebook', 'twitter', 'instagram', 'linkedin')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_draft', 'category','created_at')

admin.site.register(Blog, BlogAdmin)
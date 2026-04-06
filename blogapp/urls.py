from django.urls import path
from . import views

urlpatterns = [
    path("register_user/", views.register_user, name="register_user"),
    path("create_blog/", views.create_blog, name="create_blog"),
    path("blogs_list/", views.blog_list, name="blogs_list"),
    path("updated_blog/<int:pk>/", views.updated_blog, name="updated_blog"),
    path("delete_blog/<int:pk>/", views.delete_blog, name="delete_blog"),
    path("update_user/", views.update_user_profile, name="update_user"),
]
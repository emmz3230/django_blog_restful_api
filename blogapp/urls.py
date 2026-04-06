from django.urls import path
from . import views

urlpatterns = [
    path("register_user/", views.register_user, name="register_user"),
    path("create_blog/", views.create_blog, name="create_blog"),
    path("blogs_list/", views.blog_list, name="blogs_list"),
    path("updated_blog/", views.updated_blog, name="updated_blog"),
]
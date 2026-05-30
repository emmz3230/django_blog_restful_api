from django.urls import path
from . import views

urlpatterns = [
    path("register_user/", views.register_user, name="register_user"),
    path("create_blog/", views.create_blog, name="create_blog"),
    path("blogs_list/", views.blog_list, name="blogs_list"),
    path("blogs/<slug:slug>/", views.get_blog, name="get_blog"),
    path("update_blog/<int:pk>/", views.updated_blog, name="update_blog"),
    path("delete_blog/<int:pk>/", views.delete_blog, name="delete_blog"),
    path("update_user/", views.update_user_profile, name="update_user"),
    path("get_username", views.get_username, name="get_username"),
    path("get_userinfo/<str:username>", views.get_userinfo, name="get_userinfo"),
    path("get_user/<str:email>", views.get_user, name="get_user"),
    path("password_reset_request/", views.password_reset_request, name="password_reset_request"),
    path("password_reset_confirm/", views.password_reset_confirm, name="password_reset_confirm"),
]
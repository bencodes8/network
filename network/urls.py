
from django.urls import path

from . import views, api

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<slug:slug>", views.profile, name="profile"),
    path("user/<slug:slug>/following", views.following, name="following"),
    path("api/user/<int:user_id>", api.user_info, name="user"),
    path("api/post/<int:post_id>/edit", api.edit_post, name="post"),
    path("api/post/<int:post_id>/like", api.like_post, name="like"),
]


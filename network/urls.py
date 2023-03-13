
from django.urls import path

from . import views
from .import api

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("api/posts", api.view_all_posts, name="view_all_posts")
]

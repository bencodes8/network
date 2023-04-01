from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import User, Post

@csrf_exempt
def index(request):
    if request.user.is_authenticated and request.method == "POST":
        title = request.POST["title"]
        post = request.POST["post"]
        new_post = Post.objects.create(user=request.user, title=title, post=post)
        new_post.save()
    
    all_posts = Post.objects.all().order_by("-date")
    paginator = Paginator(all_posts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "title": "All Posts",
        "page_obj": page_obj
    })

def profile(request, slug):
    if request.user.is_authenticated:
        current_user = User.objects.get(pk=request.user.id)
    else:
        current_user = None
        
    users_profile = User.objects.get(username=slug)
    posts_profile = Post.objects.all().filter(user=users_profile.pk).order_by("-date")
    
    paginator = Paginator(posts_profile, 10)
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/profile.html", {
        "title": f"@{users_profile.username}'s Profile",
        "current_user": current_user,
        "profile": users_profile,
        "page_obj": page_obj
    })

@login_required(login_url='/login')
def following(request, slug):
    user = User.objects.get(username=slug)
    users_following = user.following.all()
    posts_following = Post.objects.filter(user__in=users_following).order_by("-date")     
    
    paginator = Paginator(posts_following, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "title": f"@{user.username}'s Following Page",
        "user": user,
        "followings": users_following,
        "page_obj": page_obj
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user}")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password.")
            return HttpResponseRedirect(reverse("login"))
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
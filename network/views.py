import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post

@csrf_exempt
def index(request): 
    # User submits a post
    if request.method == "POST" and request.user.is_authenticated:
        title = request.POST["title"]
        post = request.POST["post"]
        new_post = Post.objects.create(user=request.user, title=title, post=post)
        new_post.save()
        
    posts = Post.objects.all().order_by('-date')
    posts_data = [post.serialize() for post in posts]
    print('test')

    return render(request, "network/index.html", {
        "title": "All Posts",
        "api_route": "posts",
        "posts_json": json.dumps(posts_data),
    })

def profile(request, user_id):
    posts = Post.objects.all().filter(user=user_id)
    user = User.objects.get(pk=user_id).username
    
    
    return render(request, "network/profile.html", {
        "title": f"@{user} · Profile",
        
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
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

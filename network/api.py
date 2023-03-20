import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
from django.core.paginator import Paginator

from .models import User, Post

def view_all_posts(request):

    # Get start and end points
    start = request.GET.get('start', 0)
    end = request.GET.get('end', int(start) + 9)
    
    # Return posts as JSON
    posts = Post.objects.all().order_by('-date')[int(start):int(end)]
    serialized_posts = [post.serialize() for post in posts]
    
    return JsonResponse(serialized_posts, safe=False)

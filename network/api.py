import json
from .models import User, Post
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def user_info(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({
            "error": "User does not exist."
        }, status=400)
    
    viewing_user = User.objects.get(pk=request.user.id)
    
    viewing_user_following = viewing_user.following.all()
    
    # handle follow/unfollow 
    if request.method == "PUT":
        
        # follow user
        if user not in viewing_user_following:
            viewing_user.following.add(user)
            viewing_user.following_count += 1 # update following count
            user.followers_count += 1
        else:
        # unfollow user
            viewing_user.following.remove(user)
            viewing_user.following_count -= 1
            user.followers_count -= 1

        # save changes to the database
        viewing_user.save()
        user.save()
        
    return JsonResponse(user.serialize())

def handlePosts(id):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({
            "error": "This post does not exist."
        }, status=400)
    return post
    

@csrf_exempt
def edit_post(request, post_id):
    post = handlePosts(post_id)
    
    # handle editing of post
    if request.method == "PUT":
        data = json.loads(request.body)
        edited_post = data.get("post")
        post.post = edited_post
        post.save(update_fields=['post'])
    
    return JsonResponse(post.serialize())

@csrf_exempt
def like_post(request, post_id):
    post = handlePosts(post_id)
    user = User.objects.get(pk=request.user.id)
    
    # handle liking 
    if request.method == "PUT":
        data = json.loads(request.body)
        likes = data.get("likes")
        post.likes = likes
        
        if user not in post.liked_users.all():
            post.liked_users.add(user)
            user.liked_posts.add(post)
        else:
            post.liked_users.remove(user)
            user.liked_posts.remove(post)
            
        post.save()
        user.save()
        
    return JsonResponse(post.serialize())

    
    
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Following, Like, User, Post
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def index(request):
    current_user = request.user

    post_list = Post.objects.all().order_by("-created_at")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    
    liked_posts = []
    if current_user.is_authenticated:
           liked_posts = current_user.likes.all()
           liked_posts = [like.post for like in liked_posts]
   
    return render(request, "network/index.html", {"posts":page_posts, "liked_posts":liked_posts})



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


@login_required
@csrf_exempt
def create_post(request):
    if request.method == "POST": 
        content = request.POST["post-content"]

        if content == "":
            return JsonResponse({"error":"Post conent cannot be empty."}, status=400)
        
        post = Post(user=request.user, content=content)
        post.save()

        return redirect("index")
       
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required
@csrf_exempt
def edit_post(request, post_id): 
    if request.method == "PUT":
        user = request.user 
        body = json.loads(request.body)
        try:
          post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist: 
            return JsonResponse({"error": "Post does not exist."})
        
        if post.user != user: return JsonResponse({"error":"You are not allowed to edit the post."})
        
        post.content = body
        post.save()

        return JsonResponse({"message":"Post updated."}, status=200)



def profile_view(request, user_id):
    if request.method == "GET":    
        try:
           user = User.objects.get(pk=user_id)
           user_posts = Post.objects.filter(user=user).order_by("-created_at")

           paginator = Paginator(user_posts, 10)
           page_number = request.GET.get('page')
           page_posts = paginator.get_page(page_number)
           
           liked_posts = []
           following = []
           followers = []

           if request.user.is_authenticated:
               liked_posts = Like.objects.filter(user=request.user.id)
               liked_posts = [like.post for like in liked_posts]
    
               following = Following.objects.filter(follower=user.id)
               following = [obj.following for obj in following]
    
               followers = Following.objects.filter(following=user.id)
               followers = [obj.follower for obj in followers]

        except User.DoesNotExist:
            return JsonResponse({"error":"User does not exist."}, status=400)
        
        return render(request, "network/user_profile.html", {"user_info": user, "posts": page_posts, "liked_posts": liked_posts, "following": following, "followers":followers})
    else: 
        return HttpResponseNotAllowed(['GET'])
    
@csrf_exempt 
def follow(request, user_id):
    if request.method == "POST":
        try :
            user=User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error":"User does not exist."}, status=400)
        
        if request.user == user:
            return JsonResponse({"error": "You cannot follow yourself."}, status=400)
        
        try:
            following = Following.objects.get(follower=request.user, following=user)
            following.delete()
        except Following.DoesNotExist:
            Following.objects.create(follower=request.user, following=user)
            

        return HttpResponseRedirect(reverse("profile-view", args=[user_id]))
        
    else:
        return HttpResponseNotAllowed(['POST'])

def following_posts(request):
    current_user = request.user
    following_objects = current_user.following.all()
    posts=[]
    
    for following in following_objects:
       user_posts = Post.objects.filter(user=following.following).order_by("-created_at")
       posts.extend(list(user_posts))

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    
    liked_posts = Like.objects.filter(user=request.user)
    liked_posts = [like.post for like in liked_posts]
    
    return render(request, "network/following.html", {"posts": page_posts, "liked_posts":liked_posts})  


@csrf_exempt
def like(request, post_id):
    user = request.user 
    try:
       post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist."})
    
    if request.method == 'POST': 
       try:
           Like.objects.get(user=user, post=post)
           return JsonResponse({"error": "Post already liked."}, status=400)
       
       except Like.DoesNotExist: 
           new_like = Like.objects.create(user=user, post=post)

       return JsonResponse({"message": "Post liked successfully."}, status=201)

    elif request.method == 'DELETE': 
       try:
           existing_like = Like.objects.get(user=user, post=post)
           existing_like.delete()
           return JsonResponse({"message": "Like removed successfully."}, status=200)
       except Like.DoesNotExist:
           return JsonResponse({"error": "No like on that post to unlike."}, status=400)

    elif request.method == "GET":
        likes_count = Like.objects.filter(post=post).count()
        return JsonResponse({"counter":likes_count}, status=200)
    else:
        return JsonResponse({"error": "Only [POST, DELETE, GET] are supported."}, status=405)

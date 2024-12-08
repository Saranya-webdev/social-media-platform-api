from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

# DRF imports
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

# Models, serializers, and forms
from .models import Post, Comment, Like, Follow, UserProfile
from .serializers import PostSerializer, CommentSerializer
from .forms import PostForm, CommentForm, UserProfileForm


# Home view with pagination,profile pictures for authenticated users and authors they can follow.
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    profile_picture = None
    authors = []

    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()
        profile_picture = profile.profile_picture.url if profile and profile.profile_picture else None

        # Get all users except the current user
        authors = User.objects.exclude(id=request.user.id)  
        
        # Get the list of users that the current user is following
        following_ids = profile.following.values_list('id', flat=True)
        
        # Exclude users that the logged-in user is already following
        authors = authors.exclude(id__in=following_ids)

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'profile_picture': profile_picture,
        'authors': authors
    })


# User profile update
@login_required
def update_userprofile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile', user_id=request.user.id)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'update_userprofile.html', {'form': form})

# Update a post
@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    # Ensure only the author can update the post
    if post.author != request.user:
        return redirect('post_detail', post_id=post.id)
    
    if request.method == 'POST':
        # Update fields if provided
        image = request.FILES.get('image')
        content = request.POST.get('content')
        
        if image:
            post.image = image
        if content:
            post.content = content

        post.save()
        return redirect('post_detail', post_id=post.id)
    
    return render(request, 'post_update.html', {'post': post})

# Post creation
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'post_create.html', {'form': form})


# Post detail view with comments
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    likes_count = post.likes.count()
    # is_liked = request.user.is_authenticated and post.likes.filter(user=request.user).exists()
    is_liked = post.likes.filter(id=request.user.id).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
            messages.success(request, "Comment added successfully!")
        return redirect('post_detail', post_id=post.id)

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'likes_count': likes_count,
        'is_liked': is_liked
    })

@login_required
def edit_comment(request, comment_id):
    # Get the comment object
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure only the author can edit the comment
    if comment.author != request.user:
        messages.error(request, "You do not have permission to edit this comment.")
        return redirect('post_detail', post_id=comment.post.id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content = content  # Update the comment content
            comment.save()  # Save changes to the database
            messages.success(request, "Comment updated successfully!")
            return redirect('post_detail', post_id=comment.post.id)
        else:
            messages.error(request, "Content cannot be empty.")

    # Render the edit form
    return render(request, 'edit_comment.html', {'comment': comment})    

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id
    if comment.author == request.user:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('post_detail', post_id=post_id)
    else:
        messages.error(request, "You do not have permission to delete this comment.")    
    return redirect('post_detail', post_id=comment.post_id)     


# Like and unlike post
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        messages.info(request, "You unliked the post.")
    else:
        messages.success(request, "You liked the post.")
    
    return redirect('post_detail', post_id=post_id)


# Follow a user
def follow_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    if user_profile.user != request.user:
        if not request.user.profile.following.filter(id=user_profile.user.id).exists():
            request.user.profile.following.add(user_profile.user)
            # After following, increment the followers and following count
            user_profile.followers.add(request.user)
    return redirect('user_profile', user_id=user_id)

# Unfollow a user
def unfollow_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    if user_profile.user != request.user:
        if request.user.profile.following.filter(id=user_profile.user.id).exists():
            request.user.profile.following.remove(user_profile.user)
            # After unfollowing, decrement the followers and following count
            user_profile.followers.remove(request.user)
    return redirect('user_profile', user_id=user_id)

# Delete a post
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        post.delete()
        return redirect('home')
    return redirect('post_detail', post_id=post.id)    


# User profile view
def user_profile(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    is_following = request.user.is_authenticated and request.user.profile.following.filter(id=user_profile.user.id).exists()

    # Fetch other necessary information
    posts = Post.objects.filter(author=user_profile.user)
    post_count = posts.count()
    followers_count = user_profile.followers.count()
    following_count = user_profile.following.count()

    return render(request, 'user_profile.html', {
        'user_profile': user_profile,
        'is_following': is_following,
        'posts': posts,
        'post_count': post_count,
        'followers_count': followers_count,
        'following_count': following_count,
    })

def following_list(request, user_id):
    # Get the user profile
    user_profile = get_object_or_404(UserProfile, user__id=user_id)

    # Get all users this user is following
    following_relations = Follow.objects.filter(follower=user_profile.user)
    following = [relation.following.profile for relation in following_relations]

    return render(request, 'following_list.html', {'following': following, 'user_profile': user_profile})

def followers_list(request, user_id):
    # Get the user profile
    user_profile = get_object_or_404(UserProfile, user__id=user_id)

    # Get all followers for this user
    follower_relations = Follow.objects.filter(following=user_profile.user)
    followers = [relation.follower.profile for relation in follower_relations]

    return render(request, 'followers_list.html', {'followers': followers, 'user_profile': user_profile})

@login_required
def user_feed(request):
    # Get the list of users the current user is following
    following_users = request.user.following.values_list('following_id', flat=True)

    # Get posts from the followed users
    posts = Post.objects.filter(user__id__in=following_users).order_by('-created_at')

    # Paginate the posts
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_feed.html', {'page_obj': page_obj})    

class RegisterView(APIView):
    def get(self, request):
        # Render the registration form
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        # Handle form submission
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User registered successfully!")
            return redirect('login')  # Redirect to login page after successful registration
        else:
            # Return the form with validation errors
            return render(request, 'register.html', {'form': form})
            
# Login view
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

# Pagination for posts
class PostPagination(PageNumberPagination):
    page_size = 10 

# DRF Post viewset: Handles creating posts via an API.
class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user.profile)  # Assuming you have a profile model linked to the user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieves details of a single post.
class PostDetailView(APIView):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        return Response(PostSerializer(post).data)

# Updates post content (only accessible to the author).
class PostUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if post.author != request.user:
            return Response({"error": "You do not have permission to edit this post."}, status=403)
        
        content = request.data.get('content', post.content)
        post.content = content
        post.save()
        return Response(PostSerializer(post).data)

# Deletes a post (author only).
class PostDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if post.author != request.user:
            return Response({"error": "You do not have permission to delete this post."}, status=403)
        
        post.delete()
        return Response({"detail": "Post deleted."}, status=204)

# A DRF viewset for managing posts, supporting filtering, ordering, and search.
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['content', 'author__username']
    ordering_fields = ['created_at']   

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)                             


# Manages comments on posts using DRF
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        try:
            user_to_follow = User.objects.get(username=username)
            if user_to_follow != request.user:
                request.user.profile.following.add(user_to_follow)
                return Response({"detail": f"You are now following {user_to_follow.username}."}, status=200)
            return Response({"detail": "You cannot follow yourself."}, status=400)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user_to_unfollow = User.objects.get(username=username)
        follow_relation = Follow.objects.filter(follower=request.user.profile, following=user_to_unfollow.profile)
        
        if follow_relation.exists():
            follow_relation.delete()
            return Response({"message": "Unfollowed successfully."}, status=status.HTTP_200_OK)
        
        return Response({"message": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        # Assuming user is authenticated and you check if the user has already liked the post
        if Like.objects.filter(post=post, user=request.user).exists():
            return Response({"message": "You  unliked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        Like.objects.create(post=post, user=request.user)
        return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)          
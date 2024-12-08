from django.urls import path
from . import views  # Ensure views are correctly imported
from django.conf import settings
from django.conf.urls.static import static
from .views import (RegisterView, FollowUserView,
    UnfollowUserView,
    LikePostView,
    CommentViewSet,
    CreatePostView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,CustomLoginView, logout_view)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Post CRUD paths
    path('', views.home, name='home'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/update/', views.post_update, name='post_update'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Like a post
    # path('post/<int:post_id>/like/', views.like_post, name='like_post'),

path('post/<int:post_id>/add_comment/', views.post_detail, name='post-add_comment'),  # Handled in post_detail view

    path('post/<int:post_id>/like/', views.like_post, name='toggle_like_post'),

    # Edit profile path
    path('update-profile/', views.update_userprofile, name='update_userprofile'),
    # path('userprofile/<int:user_id>/', views.userprofile, name='user_profile'),

    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),

  path('userprofile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('userprofile/<int:user_id>/followers/', views.followers_list, name='followers_list'),
    path('userprofile/<int:user_id>/following/', views.following_list, name='following_list'),
    
   path('userprofile/<int:user_id>/', views.user_profile, name='userprofile'),

path('user/<int:user_id>/profile/', views.user_profile, name='user_profile'),
    path('user/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    path('user/<int:user_id>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('feed/', views.user_feed, name='user_feed'),

    # Authentication paths
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    # Follow and Unfollow
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow_user'),
    
    # Like and Unlike
    path('like/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    
    # Comment on Post
    # path('comment/<int:post_id>/', CommentViewSet.as_view(), name='comment_post'),
    
    # Post CRUD
    path('post/create/', CreatePostView.as_view(), name='create_post'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('post/update/<int:post_id>/', PostUpdateView.as_view(), name='update_post'),
    path('post/delete/<int:post_id>/', PostDeleteView.as_view(), name='delete_post'),
]

# Serve static and media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

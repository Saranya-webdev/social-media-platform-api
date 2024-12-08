from django.urls import path, include
from rest_framework.routers import DefaultRouter
from socialite.views import PostViewSet, CommentViewSet,FollowUserView, UnfollowUserView,LikePostView,CreatePostView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='post-comment')


urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),  # Like post URL
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('posts/create/', CreatePostView.as_view(), name='create-post'),  # Create post URL
]

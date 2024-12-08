from rest_framework import serializers
from .models import Post, Comment, Like, Follow, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(source='post', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user', 'post_id']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'image', 'created_at', 'updated_at', 'likes_count', 'comments']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(source='post', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post_id', 'created_at']


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        if data['follower'] == data['following']:
            raise serializers.ValidationError("Users cannot follow themselves.")
        return data

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']

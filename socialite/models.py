from django.db import models
from django.contrib.auth import get_user_model  #Fetches the currently active User model, supporting custom user models.
from django.contrib.auth.models import User

# UserProfile model to extend the User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') # Links UserProfile to User in a one-to-one relationship, deleting the profile when the user is deleted.

    bio = models.CharField(max_length=250, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  #Allows users to upload profile pictures, saving them in the profile_pictures/ directory.
    
    followers = models.ManyToManyField(User, related_name='user_followers', blank=True) # Creates a many-to-many relationship for followers of a user.

    following = models.ManyToManyField(User, related_name='user_following', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# Post model to store posts made by users
class Post(models.Model):
    content = models.TextField(blank=True)

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts') # Links the Post to the user who created it, and deletes the post if the user is deleted.

    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True) # Automatically sets the date and time when the object is created.

    updated_at = models.DateTimeField(auto_now=True)
   

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at}'

# Comment model to store comments on posts
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) # Links a Comment to a Post, enabling reverse access to all comments for a post.

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.id}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']

# Like model to store likes on posts
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='liked_posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post') #Ensures that a user can like a post only once.

    def __str__(self):
        return f'{self.user.username} liked {self.post.id}' #Provides a human-readable string representation of the Like object.

# Follow model to store followers and following relationships
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate follows

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"



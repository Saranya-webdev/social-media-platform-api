from django import forms
from .models import Post, Comment, UserProfile
from django.core.exceptions import ValidationError
import os

# Post form for creating and editing posts
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your post here...',
                'rows': 4,
                'class': 'form-control'  # Add Bootstrap class for better styling (optional)
            }),
        }
        error_messages = {
            'content': {
                'required': 'Please write something before submitting.',
            },
            'image': {
                'invalid': 'Upload a valid image file.',
            },
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('An image is required for the post.')        
        return image


# Comment form for creating and editing comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Add a comment...',
                'rows': 3,
                'class': 'form-control'
            }),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('This field cannot be empty.')
        if len(content) < 10:
            raise forms.ValidationError('Comment should be at least 10 characters long.')
        if len(content) > 500:  # Example: Set a maximum length for comments
            raise forms.ValidationError('Comment cannot exceed 500 characters.')
        # Optional: Add further checks like inappropriate language or HTML sanitization
        return content


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if len(bio) > 500:
            raise forms.ValidationError('Bio cannot exceed 500 characters.')
        return bio

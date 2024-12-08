Social Media Platform API
This project is a Django-based social media platform API that allows users to perform CRUD operations on user profiles, posts, likes, and comments. Users can also follow and unfollow each other. The project is built using Django and MySQL and provides an API using Django REST Framework.

Project Structure
The project consists of two main directories: the project directory (social_media) and the app directory (socialite). Below is an overview of the project structure:

1. Project Directory (social_media)
asgi.py: Configuration for ASGI.
settings.py: Settings for the project, including database configuration, installed apps, and middleware.
urls.py: Main URL routing for the project.
wsgi.py: Configuration for WSGI.
2. App Directory (socialite)
This directory contains the application that powers the social media functionality.

admin.py: Customizes the admin interface for the socialite app.
api_urls.py: API routes for the social media features.
apps.py: Application configuration.
forms.py: Forms used for handling user data (e.g., registration and profile updates).
models.py: Defines the models for user profiles, posts, comments, likes, and follow relationships.
serializers.py: Serializers to convert model instances to JSON format.
signals.py: Signals for automatic actions like creating a user profile when a new user is created.
tests.py: Test cases for the app.
urls.py: URL routing for the socialite app.
views.py: Views for handling business logic and API responses.
3. Templates Directory (socialite/templates)
Contains HTML templates used for rendering views in the app. Includes the following:

base.html: The base template.
edit_comment.html: Template for editing comments.
followers_list.html: List of followers.
following_list.html: List of users the current user is following.
home.html: Home page for the user feed.
post_create.html: Template for creating new posts.
post_detail.html: View for post details.
post_update.html: Template for updating a post.
register.html: User registration page.
update_userprofile.html: Template for updating user profile information.
user_feed.html: User's personalized feed.
user_profile.html: User profile page.
4. Static Directory (socialite/static)
Contains static files such as CSS and images.

css/styles.css: Stylesheet for the app.
images/default.png: Default profile picture.
Requirements
Python 3.x
Django 3.x or above
MySQL
Django REST Framework
Django CORS Headers (for cross-origin requests)
Setup Instructions
1. Clone the Repository
Clone the repository to your local machine:

git clone https://github.com/yourusername/social-media-platform-api.git
cd social-media-platform-api

# 2. Install Dependencies
# Install the required Python packages using pip:
pip install -r requirements.txt

# 3. Configure MySQL Database
# 1.Create a MySQL database for the project:
CREATE DATABASE social_media_db;

# 2. Update the DATABASES settings in social_media/settings.py to use MySQL:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'social_media_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# 4. Run Migrations
# Apply the migrations to set up the database schema:

python manage.py makemigrations
python manage.py migrate

# 5. Create a Superuser
# To access the admin panel, create a superuser:
python manage.py createsuperuser

# 6. Start the Development Server
# Run the development server:
python manage.py runserver
# Your application will be available at http://127.0.0.1:8000/.


# API Endpoints
# Authentication :
POST /api/auth/register/: Register a new user.
POST /api/auth/login/: Log in and get a token for authentication.
User Profile
GET /api/users/me/: Get the current user’s profile.
PATCH /api/users/me/: Update the current user’s profile.
Posts
POST /api/posts/: Create a new post.
GET /api/posts/: List all posts.
GET /api/posts/{id}/: Get details of a specific post.
PUT /api/posts/{id}/: Update a post.
DELETE /api/posts/{id}/: Delete a post.
Comments
POST /api/posts/{id}/comments/: Add a comment to a post.
GET /api/posts/{id}/comments/: Get all comments for a post.
Likes
POST /api/posts/{id}/like/: Like a post.
POST /api/posts/{id}/unlike/: Unlike a post.
Follow/Unfollow Users
POST /api/follow/{username}/: Follow a user.
POST /api/unfollow/{username}/: Unfollow a user

# Testing
# To run tests:
python manage.py test

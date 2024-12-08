from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include the API URLs directly from api_urls.py
    path('api/', include('socialite.api_urls')),  # Correctly include the api_urls.py

    # Include socialite application routes for user interaction
    path('', include('socialite.urls')),  # Include the app's URLs
]

document.addEventListener('DOMContentLoaded', function () {

    // Toggle Like functionality
    function toggleLike(postId) {
        const likeButton = document.getElementById('like-btn-' + postId);
        const likeCount = document.getElementById('like-count-' + postId);

        // Disable button to prevent multiple submissions
        likeButton.disabled = true;

        fetch(`/toggle_like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.liked) {
                likeButton.textContent = "Unlike";
                likeCount.textContent = `Likes(${data.likes_count})`;
            } else {
                likeButton.textContent = "Like";
                likeCount.textContent = `Likes(${data.likes_count})`;
            }
            likeButton.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            likeButton.disabled = false;
        });
    }

    // Toggle Follow functionality
    function toggleFollow(authorId) {
        const followButton = document.getElementById('follow-btn-' + authorId);

        // Disable button to prevent multiple submissions
        followButton.disabled = true;

        fetch(`/toggle_follow/${authorId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.following) {
                followButton.textContent = "Unfollow";
            } else {
                followButton.textContent = "Follow";
            }
            followButton.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            followButton.disabled = false;
        });
    }

    // Toggle comment form visibility
    function toggleComment(postId) {
        const commentSection = document.getElementById('comment-section-' + postId);
        commentSection.style.display = commentSection.style.display === 'none' ? 'block' : 'none';
    }

    // Submit comment for a post
    function submitComment(postId) {
        const commentInput = document.getElementById('comment-input-' + postId);
        const commentContent = commentInput.value;

        if (!commentContent.trim()) {
            alert('Please enter a comment.');
            return;
        }

        // Disable the comment input to prevent multiple submissions
        commentInput.disabled = true;

        fetch(`/api/posts/${postId}/add_comment/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ content: commentContent })
        })
        .then(response => response.json())
        .then(data => {
            // Successfully added comment
            const commentList = document.getElementById('comment-list-' + postId);
            const newComment = document.createElement('div');
            newComment.textContent = data.content;
            commentList.appendChild(newComment);

            // Clear input and re-enable it
            commentInput.value = '';
            commentInput.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            commentInput.disabled = false;
        });
    }

    // Helper function to get CSRF token for AJAX requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Image preview
    const imageInput = document.getElementById('id_image');
    const imagePreview = document.getElementById('image-preview');
    imageInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.innerHTML = `<img src="${e.target.result}" alt="Image Preview" style="max-width: 300px;">`;
        };
        reader.readAsDataURL(file);
    });

    // Character counter for the content textarea
    const contentTextarea = document.getElementById('id_content');
    const characterCount = document.getElementById('character-count');
    contentTextarea.addEventListener('input', () => {
        characterCount.textContent = contentTextarea.value.length;
    });
});

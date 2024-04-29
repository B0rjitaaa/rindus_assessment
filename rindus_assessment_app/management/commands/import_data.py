from django.core.management.base import BaseCommand
from ...models import Post, Comment
import requests
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import data from JSONPlaceholder'

    def handle(self, *args, **kwargs):        
        try:
            # Fetch posts from JSONPlaceholder
            posts_response = requests.get('https://jsonplaceholder.typicode.com/posts')
            posts_response.raise_for_status()  # Raise an exception for HTTP errors
            posts_data = posts_response.json()

            if not posts_data:
                logger.warning("No posts data received from JSONPlaceholder")
                return

            # Create Post objects
            for post_data in posts_data:
                try:
                    post = Post.objects.create(
                        title=post_data['title'],
                        body=post_data['body']
                    )

                    # Fetch comments for each post
                    comments_response = requests.get(f'https://jsonplaceholder.typicode.com/posts/{post_data["id"]}/comments')
                    comments_response.raise_for_status()  # Raise an exception for HTTP errors
                    comments_data = comments_response.json()

                    # Create Comment objects for each post
                    for comment_data in comments_data:
                        Comment.objects.create(
                            post=post,
                            name=comment_data['name'],
                            email=comment_data['email'],
                            body=comment_data['body']
                        )
                except Exception as e:
                    logger.error(f"Error processing post data: {e}")
        except requests.RequestException as e:
            logger.error(f"Error fetching data from JSONPlaceholder: {e}")
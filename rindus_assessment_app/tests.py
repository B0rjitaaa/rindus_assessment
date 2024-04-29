from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post, Comment

from django.core.management import call_command
from unittest.mock import patch, MagicMock


class APITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')


    def test_create_post(self):
        url = '/posts/'
        data = {'title': 'Test Post', 'body': 'This is a test post content.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Test Post')


    def test_retrieve_post(self):
        post = Post.objects.create(title='Test Post', body='This is a test post content.')
        url = f'/posts/{post.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')


    def test_update_post(self):
        post = Post.objects.create(title='Test Post', body='This is a test post content.')
        url = f'/posts/{post.id}/'
        data = {'title': 'Updated Test Post', 'body': 'Updated test post content.'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get().title, 'Updated Test Post')
    

    def test_partial_update_post(self):
        post = Post.objects.create(title='Test Post', body='This is a test post content.')
        url = f'/posts/{post.id}/'
        data = {'title': 'Updated Test Post'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get().title, 'Updated Test Post')
    

    def test_delete_post(self):
        post = Post.objects.create(title='Test Post', body='This is a test post content.')
        url = f'/posts/{post.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    
    def test_create_comment(self):
        post = Post.objects.create(title='Test Post', body='This is a test post body.')
        url = f'/comments/'
        data = {'name': 'Test User', 'email': 'test@example.com', 'body': 'This is a test comment.', 'post': post.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().name, 'Test User')


    def test_retrieve_comment(self):
        post = Post.objects.create(title='Test Post', body='This is a test post body.', user_id=1)
        comment = Comment.objects.create(post=post, name='Test User', email='test@example.com', body='This is a test comment.')
        url = f'/comments/{comment.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test User')

    
    def test_update_comment(self):
        post = Post.objects.create(title='Test Post', body='This is a test post body.', user_id=1)
        comment = Comment.objects.create(post=post, name='Test User', email='test@example.com', body='This is a test comment.')
        url = f'/comments/{comment.id}/'
        data = {'name': 'Updated Test User', 'body': 'Updated test comment body.', 'email': 'new_email@test.es', 'post': post.pk}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get().name, 'Updated Test User')


    def test_delete_comment(self):
        post = Post.objects.create(title='Test Post', body='This is a test post body.', user_id=1)
        comment = Comment.objects.create(post=post, name='Test User', email='test@example.com', body='This is a test comment.')
        url = f'/comments/{comment.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)


class ImportDataCommandTest(TestCase):
    @patch('rindus_assessment_app.management.commands.import_data.requests.get')
    def test_handle_command_success(self, mock_get):
        # Mock the response from JSONPlaceholder
        posts_response_mock = MagicMock()
        posts_response_mock.json.return_value = [
            {'id': 1, 'title': 'Test Post 1', 'body': 'This is a test post body 1'},
        ]
        comments_response_mock = MagicMock()
        comments_response_mock.json.side_effect = [
            [{'name': 'Test Comment 1', 'email': 'test1@example.com', 'body': 'This is a test comment body 1'}],
        ]
        mock_get.side_effect = [posts_response_mock, comments_response_mock]

        # Call the command
        call_command('import_data')

        # Assert that Post and Comment objects were created
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class TestView(APITestCase):
    # POST test
    def test_creating_a_tag(self):
        text = {"text": "test_tag"}
        response = self.client.post(reverse('tag_create_or_get_all'), text)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creating_user(self):
        user = {"email": "email", "password": "password", "nickname": "nickname"}
        response = self.client.post(reverse('user_create_or_get_all'), user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creating_a_post_with_invalid_data(self):
        # create an example tag for testing
        text_post = {"text": "test_tag"}
        self.client.post(reverse('tag_create_or_get_all'), text_post)
        # create an example user for testing
        user_post = {"email": "email", "password": "password", "nickname": "nickname"}
        self.client.post(reverse('user_create_or_get_all'), user_post)

        # create post
        post_post = {"topic": "post_topic", "text": "Simple text",
                     "likes": 20, "dislikes": 10, "user_id": 1,
                     "tags": ["test_tag"]}
        response = self.client.post(reverse('create_or_get_alL_posts'), post_post)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_a_post_with_negative_likes(self):
        # create an example tag for testing
        text_post = {"text": "test_tag"}
        self.client.post(reverse('tag_create_or_get_all'), text_post)
        # create an example user for testing
        user_post = {"email": "email", "password": "password", "nickname": "nickname"}
        self.client.post(reverse('user_create_or_get_all'), user_post)

        # create post
        post_post = {"topic": "post_topic", "text": "Simple text",
                     "likes": -1, "dislikes": 2, "user_id": 1,
                     "tags": ["test_tag"]}
        response = self.client.post(reverse('create_or_get_alL_posts'), post_post)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_a_comment(self):
        # create an example tag for testing
        text = {"text": "test_tag"}
        self.client.post(reverse('tag_create_or_get_all'), text)
        # create an example user for testing
        user = {"email": "email", "password": "password", "nickname": "nickname"}
        self.client.post(reverse('user_create_or_get_all'), user)

        # create post
        post = {"topic": "post_topic", "text": "Simple text",
                "likes": 20, "dislikes": 10, "user_id": 1,
                "tags": ["test_tag"]}
        self.client.post(reverse('create_or_get_alL_posts'), post)
        # create a comment
        comment = {"post": 1, "text": "text", "user_id": 1, "likes": 5, "dislikes": 3}
        response = self.client.post(reverse('create_comment', args=['1']), comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # GET test
    def test_all_post(self):
        response = self.client.get(reverse('create_or_get_alL_posts'))
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_get_certain_post(self):
        # create an example tag for testing
        text = {"text": "test_tag"}
        self.client.post(reverse('tag_create_or_get_all'), text)
        # create an example user for testing
        user = {"email": "email", "password": "password", "nickname": "nickname"}
        self.client.post(reverse('user_create_or_get_all'), user)

        # create post
        post = {"topic": "post_topic", "text": "Simple text",
                "likes": 20, "dislikes": 10, "user_id": 1,
                "tags": ["test_tag"]}
        self.client.post(reverse('create_or_get_alL_posts'), post)
        response = self.client.get(reverse('get_certain_post', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_get_all_tags(self):
        # create an example tag for testing
        text = {"text": "test_tag"}
        self.client.post(reverse('tag_create_or_get_all'), text)
        response = self.client.get(reverse('tag_create_or_get_all'))
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)


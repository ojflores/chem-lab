from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

import json


class RegisterTest(APITestCase):
    def setUp(self):
        self.view_name = 'register:register'

    def test_register_new_user(self):
        # request
        request_body = {
            'password': 'SeCure-passw0rD589',
            'email': 'bob.joe@wallawalla.edu',
            'first_name': 'Bob',
            'last_name': 'Joe',
        }
        response = self.client.post(reverse(self.view_name), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=request_body['email'],
                                            first_name=request_body['first_name'],
                                            last_name=request_body['last_name']).exists())
        # test response
        self.assertEqual(response_body['username'], request_body['email'].split('@')[0])
        self.assertTrue('password' not in response_body.keys())
        self.assertEqual(response_body['email'], request_body['email'])
        self.assertEqual(response_body['first_name'], request_body['first_name'])
        self.assertEqual(response_body['last_name'], request_body['last_name'])

    def test_register_duplicate_email(self):
        # add user
        first_user = User.objects.create_user(password='password',
                                              email='bob.joe@wallawalla.edu',
                                              username='bob.joe')
        first_user.save()
        # request
        request_body = {
            'password': 'SeCure-passw0rD589',
            'email': first_user.email,
            'first_name': 'Bob',
            'last_name': 'Joe',
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # test database
        self.assertEqual(len(User.objects.all()), 1)

    def test_register_bad_email(self):
        # request
        request_body = {
            'password': 'SeCure-passw0rD589',
            'email': 'bad.email@other.com',
            'first_name': 'Bob',
            'last_name': 'Joe',
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # test database
        self.assertFalse(User.objects.filter(email=request_body['email'],
                                             first_name=request_body['first_name'],
                                             last_name=request_body['last_name']).exists())

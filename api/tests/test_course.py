from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from api.models import Course


class TestCourseLCPost(APITestCase):
    '''
    Test cases for POST requests on CourseLCView.
    '''
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='add_course'))
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'api:course-lc'

    def test_course_create(self):
        '''
        Tests that a course is properly created.
        '''
        # create a course
        request_body = {
            'name': 'test name'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        course = Course.objects.first()
        # test database
        self.assertEqual(course.name, request_body['name'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['name'], request_body['name'])


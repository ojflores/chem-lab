from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from api.models import Course


class TestCourseLC(APITestCase):
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
        # request
        request_body = {
            'name': 'test name'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        course = Course.objects.first()
        self.assertEqual(course.name, request_body['name'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['name'], request_body['name'])

    def test_course_list(self):
        '''
        Tests that courses are properly listed.
        '''
        # add courses to database
        Course(name='test name 1').save()
        Course(name='test name 2').save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        courses = Course.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['courses'][0]['name'], courses[0].name)
        self.assertEqual(response_body['courses'][1]['name'], courses[1].name)


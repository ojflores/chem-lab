from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from api.models import Course


class CourseLCTest(APITestCase):
    '''
    Test cases for list and create requests on CourseLCView.
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
        self.assertEqual(response_body['pk'], course.id)
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
        self.assertEqual(response_body['courses'][0]['pk'], courses[0].id)
        self.assertEqual(response_body['courses'][0]['name'], courses[0].name)
        self.assertEqual(response_body['courses'][1]['pk'], courses[1].id)
        self.assertEqual(response_body['courses'][1]['name'], courses[1].name)


class CourseRUDTest(APITestCase):
    '''
    Test cases for request, update, and destroy requests on CourseRUDView.
    '''
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='change_course'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_course'))
        self.client.login(username=self.username, password=self.password)
        # add courses to database
        self.course_1 = Course(name='test name 1')
        self.course_1.save()
        self.course_2 = Course(name='test name 2')
        self.course_2.save()
        self.course_3 = Course(name='test name 3')
        self.course_3.save()
        # retrieve the view
        self.view_name = 'api:course-rud'

    def test_course_retrieve(self):
        '''
        Tests that a course is properly retrieved.
        '''
        # request
        response = self.client.get(reverse(self.view_name, args=[self.course_2.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.course_2.id)
        self.assertEqual(response_body['name'], self.course_2.name)

    def test_course_update(self):
        '''
        Tests that a course is properly updated.
        '''
        # modify values
        request_body = {
            'name': 'name changed',
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.course_2.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        course = Course.objects.filter(name=request_body['name']).first()
        self.assertEqual(course.id, self.course_2.id)
        self.assertEqual(course.name, request_body['name'])
        # test repsonse
        self.assertEqual(response_body['pk'], self.course_2.id)
        self.assertEqual(response_body['name'], request_body['name'])


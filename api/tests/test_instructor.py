from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from api.models import Instructor


class InstructorLCTest(APITestCase):
    """
    Test cases for list and create requests on InstructorLCView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.username_2 = 'test 2'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user_2 = User.objects.create_user(username=self.username_2, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='add_instructor'))
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'api:instructor-lc'

    def test_instructor_create(self):
        """
        Tests that a instructor is properly created.
        """
        # request
        request_body = {
            'wwuid': '1111111',
            'user': self.user.id
        }
        response = self.client.post(reverse(self.view_name), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        instructor = Instructor.objects.first()
        self.assertEqual(instructor.wwuid, request_body['wwuid'])
        self.assertEqual(instructor.user.id, request_body['user'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['pk'], instructor.id)
        self.assertEqual(response_body['wwuid'], request_body['wwuid'])
        self.assertEqual(response_body['user'], request_body['user'])

    def test_instructor_list(self):
        """
        Tests that instructors are properly listed.
        """
        # add courses to database
        Instructor(wwuid='wwuid 1', user=self.user).save()
        Instructor(wwuid='wwuid 2', user=self.user_2).save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        instructors = Instructor.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['instructors'][0]['pk'], instructors[0].id)
        self.assertEqual(response_body['instructors'][0]['wwuid'], instructors[0].wwuid)
        self.assertEqual(response_body['instructors'][0]['user'], instructors[0].user.id)
        self.assertEqual(response_body['instructors'][1]['pk'], instructors[1].id)
        self.assertEqual(response_body['instructors'][1]['wwuid'], instructors[1].wwuid)
        self.assertEqual(response_body['instructors'][1]['user'], instructors[1].user.id)


class InstructorRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on InstructorRUDView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test 1'
        self.username_2 = 'test 2'
        self.username_3 = 'test 3'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user_2 = User.objects.create_user(username=self.username_2, password=self.password)
        self.user_3 = User.objects.create_user(username=self.username_3, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='change_instructor'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_instructor'))
        self.client.login(username=self.username, password=self.password)
        # add courses to database
        self.instructor_1 = Instructor(wwuid='wwuid 1', user=self.user)
        self.instructor_1.save()
        self.instructor_2 = Instructor(wwuid='wwuid 2', user=self.user_2)
        self.instructor_2.save()
        self.instructor_3 = Instructor(wwuid='wwuid 3', user=self.user_3)
        self.instructor_3.save()
        # retrieve the view
        self.view_name = 'api:instructor-rud'

    def test_instructor_retrieve(self):
        """
        Tests that a instructor is properly retrieved.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.instructor_2.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.instructor_2.id)
        self.assertEqual(response_body['wwuid'], self.instructor_2.wwuid)
        self.assertEqual(response_body['user'], self.instructor_2.user.id)

    def test_instructor_update(self):
        """
        Tests that an instructor is properly updated.
        """
        # modify values
        request_body = {
            'user': self.instructor_2.user.id,
            'wwuid': 'changed'
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.instructor_2.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        instructor = Instructor.objects.filter(id=self.instructor_2.id).first()
        self.assertEqual(instructor.id, self.instructor_2.id)
        self.assertEqual(instructor.wwuid, request_body['wwuid'])
        self.assertEqual(instructor.user.id, request_body['user'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.instructor_2.id)
        self.assertEqual(response_body['wwuid'], request_body['wwuid'])
        self.assertEqual(response_body['user'], request_body['user'])

    def test_instructor_destroy(self):
        """
        Tests that a instructor is properly destroyed.
        """
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.instructor_2.id]))
        # test database
        instructors = Instructor.objects.all()
        self.assertTrue(self.instructor_1 in instructors)
        self.assertTrue(self.instructor_2 not in instructors)
        self.assertTrue(self.instructor_3 in instructors)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

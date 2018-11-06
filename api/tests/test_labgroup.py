from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from api.models import Course, Instructor, LabGroup


class LabGroupLCTest(APITestCase):
    """
    Test cases for list and create requests on LabGroupView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='add_labgroup'))
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'api:labgroup-lc'

        # Create foreign keys
        self.instructor = Instructor(user=self.user, wwuid="1234567")
        self.instructor.save()
        self.course = Course(name="test_course")
        self.course.save()

    def test_labgroup_create(self):
        """
        Tests that a labgroup is properly created.
        """

        # request
        request_body = {
            'course': self.course.id,
            'instructor': self.instructor.id,
            'term': 'test term',
            'enroll_key': 'test enroll_key',

        }
        response = self.client.post(reverse(self.view_name), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        labgroup = LabGroup.objects.first()
        self.assertEqual(labgroup.course, self.course)
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['pk'], labgroup.id)
        self.assertEqual(response_body['course'], request_body['course'])
        self.assertEqual(response_body['instructor'], request_body['instructor'])
        self.assertEqual(response_body['term'], request_body['term'])
        self.assertEqual(response_body['enroll_key'], request_body['enroll_key'])

    def test_labgroup_list(self):
        """
        Tests that labgroups are properly listed.
        """
        # add labgroups to database
        Course(name='test name 1').save()
        Course(name='test name 2').save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        labgroups = Course.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['labgroups'][0]['pk'], labgroups[0].id)
        self.assertEqual(response_body['labgroups'][0]['name'], labgroups[0].name)
        self.assertEqual(response_body['labgroups'][1]['pk'], labgroups[1].id)
        self.assertEqual(response_body['labgroups'][1]['name'], labgroups[1].name)


class CourseRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on CourseRUDView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='change_labgroup'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_labgroup'))
        self.client.login(username=self.username, password=self.password)
        # add labgroups to database
        self.labgroup_1 = Course(name='test name 1')
        self.labgroup_1.save()
        self.labgroup_2 = Course(name='test name 2')
        self.labgroup_2.save()
        self.labgroup_3 = Course(name='test name 3')
        self.labgroup_3.save()
        # retrieve the view
        self.view_name = 'api:labgroup-rud'

    def test_labgroup_retrieve(self):
        """
        Tests that a labgroup is properly retrieved.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.labgroup_2.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.labgroup_2.id)
        self.assertEqual(response_body['name'], self.labgroup_2.name)

    def test_labgroup_update(self):
        """
        Tests that a labgroup is properly updated.
        """
        # modify values
        request_body = {
            'name': 'name changed',
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.labgroup_2.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        labgroup = Course.objects.filter(name=request_body['name']).first()
        self.assertEqual(labgroup.id, self.labgroup_2.id)
        self.assertEqual(labgroup.name, request_body['name'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.labgroup_2.id)
        self.assertEqual(response_body['name'], request_body['name'])

    def test_labgroup_destroy(self):
        """
        Tests that a labgroup is properly destroyed.
        """
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.labgroup_2.id]))
        # test database
        labgroups = Course.objects.all()
        self.assertTrue(self.labgroup_1 in labgroups)
        self.assertTrue(self.labgroup_2 not in labgroups)
        self.assertTrue(self.labgroup_3 in labgroups)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

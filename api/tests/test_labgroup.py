from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from api.models import Course, Instructor, LabGroup


class LabGroupLCTest(APITestCase):
    """
    Test cases for list and create requests on LabGroupLCView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='add_labgroup'))
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'api:lab-group-lc'
        # Create foreign keys
        self.instructor = Instructor(user=self.user, wwuid="1234567")
        self.instructor.save()
        self.course = Course(name="test_course")
        self.course.save()

    def test_lab_group_create(self):
        """
        Tests that a lab group is properly created.
        """
        # request
        request_body = {
            'course': self.course.id,
            'instructor': self.instructor.id,
            'group_name': 'test name',
            'term': 'test term',
            'enroll_key': 'test enroll_key',
        }
        response = self.client.post(reverse(self.view_name), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        lab_group = LabGroup.objects.first()
        self.assertEqual(lab_group.course.id, request_body['course'])
        self.assertEqual(lab_group.instructor.id, request_body['course'])
        self.assertEqual(lab_group.group_name, request_body['group_name'])
        self.assertEqual(lab_group.term, request_body['term'])
        self.assertEqual(lab_group.enroll_key, request_body['enroll_key'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['pk'], lab_group.id)
        self.assertEqual(response_body['course'], request_body['course'])
        self.assertEqual(response_body['instructor'], request_body['instructor'])
        self.assertEqual(response_body['group_name'], request_body['group_name'])
        self.assertEqual(response_body['term'], request_body['term'])
        self.assertEqual(response_body['enroll_key'], request_body['enroll_key'])

    def test_lab_group_list(self):
        """
        Tests that lab groups are properly listed.
        """
        # add lab groups to database
        LabGroup(course=self.course,
                 instructor=self.instructor,
                 group_name='test name 1',
                 term='test1',
                 enroll_key='test key 1').save()
        LabGroup(course=self.course,
                 instructor=self.instructor,
                 group_name='test name 2',
                 term='test2',
                 enroll_key='test key 2').save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        lab_groups = LabGroup.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['lab_groups'][0]['pk'], lab_groups[0].id)
        self.assertEqual(response_body['lab_groups'][0]['course'], lab_groups[0].course.id)
        self.assertEqual(response_body['lab_groups'][0]['instructor'], lab_groups[0].instructor.id)
        self.assertEqual(response_body['lab_groups'][0]['group_name'], lab_groups[0].group_name)
        self.assertEqual(response_body['lab_groups'][0]['enroll_key'], lab_groups[0].enroll_key)
        self.assertEqual(response_body['lab_groups'][0]['term'], lab_groups[0].term)
        self.assertEqual(response_body['lab_groups'][1]['pk'], lab_groups[1].id)
        self.assertEqual(response_body['lab_groups'][1]['course'], lab_groups[1].course.id)
        self.assertEqual(response_body['lab_groups'][1]['instructor'], lab_groups[1].instructor.id)
        self.assertEqual(response_body['lab_groups'][1]['group_name'], lab_groups[1].group_name)
        self.assertEqual(response_body['lab_groups'][1]['enroll_key'], lab_groups[1].enroll_key)
        self.assertEqual(response_body['lab_groups'][1]['term'], lab_groups[1].term)


class LabGroupRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on LabGroupRUDView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='add_labgroup'))
        self.client.login(username=self.username, password=self.password)
        # Create foreign keys
        self.instructor = Instructor(user=self.user, wwuid="1234567")
        self.instructor.save()
        self.course_1 = Course(name="test course 1")
        self.course_1.save()
        self.course_2 = Course(name="test course 2")
        self.course_2.save()
        # add lab groups to database
        self.lab_group_1 = LabGroup(course=self.course_1,
                                    instructor=self.instructor,
                                    term='test1',
                                    enroll_key='test key 1')
        self.lab_group_1.save()
        self.lab_group_2 = LabGroup(course=self.course_1,
                                    instructor=self.instructor,
                                    term='test2',
                                    enroll_key='test key 2')
        self.lab_group_2.save()
        self.lab_group_3 = LabGroup(course=self.course_1,
                                    instructor=self.instructor,
                                    term='test3',
                                    enroll_key='test key 3')
        self.lab_group_3.save()
        # retrieve the view
        self.view_name = 'api:lab-group-rud'

    def test_lab_group_retrieve(self):
        """
        Tests that a lab group is properly retrieved.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.lab_group_2.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.lab_group_2.id)
        self.assertEqual(response_body['course'], self.lab_group_2.course.id)
        self.assertEqual(response_body['term'], self.lab_group_2.term)
        self.assertEqual(response_body['group_name'], self.lab_group_2.group_name)
        self.assertEqual(response_body['instructor'], self.lab_group_2.instructor.id)
        self.assertEqual(response_body['enroll_key'], self.lab_group_2.enroll_key)

    def test_lab_group_update(self):
        """
        Tests that a lab group is properly updated.
        """
        # modify values
        request_body = {
            'course': self.course_2.id,
            'instructor': self.instructor.id,
            'group_name': 'changed',
            'term': 'changed',
            'enroll_key': 'changed',
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.lab_group_2.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        lab_group = LabGroup.objects.filter(term=request_body['term']).first()
        self.assertEqual(lab_group.id, self.lab_group_2.id)
        self.assertEqual(lab_group.course.id, request_body['course'])
        self.assertEqual(lab_group.group_name, request_body['group_name'])
        self.assertEqual(lab_group.instructor.id, request_body['instructor'])
        self.assertEqual(lab_group.term, request_body['term'])
        self.assertEqual(lab_group.enroll_key, request_body['enroll_key'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.lab_group_2.id)
        self.assertEqual(response_body['course'], request_body['course'])
        self.assertEqual(response_body['group_name'], request_body['group_name'])
        self.assertEqual(response_body['instructor'], request_body['instructor'])
        self.assertEqual(response_body['term'], request_body['term'])
        self.assertEqual(response_body['enroll_key'], request_body['enroll_key'])

    def test_lab_group_destroy(self):
        """
        Tests that a lab group is properly destroyed.
        """
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.lab_group_2.id]))
        # test database
        lab_groups = LabGroup.objects.all()
        self.assertTrue(self.lab_group_1 in lab_groups)
        self.assertTrue(self.lab_group_2 not in lab_groups)
        self.assertTrue(self.lab_group_3 in lab_groups)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

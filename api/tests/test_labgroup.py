from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from api import permissions
from api.models import Course, Instructor, LabGroup
from api.views import get_current_term


class LabGroupLCTest(APITestCase):
    """
    Test cases for list and create requests on LabGroupLCView.
    """
    def setUp(self):
        # create test user with permissions
        self.instructor_username = 'instructor'
        self.student_username = 'student'
        self.password = 'test'
        self.instructor_user = User.objects.create_user(username=self.instructor_username, password=self.password)
        self.student_user = User.objects.create_user(username=self.student_username, password=self.password)
        self.instructor_user.groups.add(permissions.get_or_create_instructor_permissions())
        self.student_user.groups.add(permissions.get_or_create_student_permissions())
        self.client.login(username=self.instructor_username, password=self.password)
        # retrieve the view
        self.view_name = 'api:lab-group-lc'
        # Create foreign keys
        self.instructor = Instructor(user=self.instructor_user, wwuid="1234567")
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
            'group_name': 'test name',
            'term': 'FALL2000',
            'enroll_key': 'test enroll_key',
        }
        response = self.client.post(reverse(self.view_name), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        labgroup = LabGroup.objects.first()
        self.assertEqual(labgroup.course.id, request_body['course'])
        self.assertEqual(labgroup.instructor.id, request_body['instructor'])
        self.assertEqual(labgroup.group_name, request_body['group_name'])
        self.assertEqual(labgroup.term, request_body['term'])
        self.assertEqual(labgroup.enroll_key, request_body['enroll_key'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['pk'], labgroup.id)
        self.assertEqual(response_body['course'], request_body['course'])
        self.assertEqual(response_body['instructor'], request_body['instructor'])
        self.assertEqual(response_body['group_name'], request_body['group_name'])
        self.assertEqual(response_body['term'], request_body['term'])
        self.assertEqual(response_body['enroll_key'], request_body['enroll_key'])

    def test_labgroup_list_instructor(self):
        """
        Tests that labgroups are properly listed for instructors.
        """
        # add labgroups to database
        LabGroup(course=self.course,
                 instructor=self.instructor,
                 group_name='test name 1',
                 term=get_current_term(),
                 enroll_key='test key 1').save()
        LabGroup(course=self.course,
                 instructor=self.instructor,
                 group_name='test name 2',
                 term=get_current_term(),
                 enroll_key='test key 2').save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        labgroups = LabGroup.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['labgroups'][0]['pk'], labgroups[0].id)
        self.assertEqual(response_body['labgroups'][0]['course'], labgroups[0].course.id)
        self.assertEqual(response_body['labgroups'][0]['instructor'], labgroups[0].instructor.id)
        self.assertEqual(response_body['labgroups'][0]['group_name'], labgroups[0].group_name)
        self.assertEqual(response_body['labgroups'][0]['enroll_key'], labgroups[0].enroll_key)
        self.assertEqual(response_body['labgroups'][0]['term'], labgroups[0].term)
        self.assertEqual(response_body['labgroups'][1]['pk'], labgroups[1].id)
        self.assertEqual(response_body['labgroups'][1]['course'], labgroups[1].course.id)
        self.assertEqual(response_body['labgroups'][1]['instructor'], labgroups[1].instructor.id)
        self.assertEqual(response_body['labgroups'][1]['group_name'], labgroups[1].group_name)
        self.assertEqual(response_body['labgroups'][1]['enroll_key'], labgroups[1].enroll_key)
        self.assertEqual(response_body['labgroups'][1]['term'], labgroups[1].term)

    def test_labgroup_list_student(self):
        """
        Tests that labgroups are properly listed for students.
        """
        # add labgroups to database
        LabGroup(course=self.course,
                 instructor=self.instructor,
                 group_name='test name 1',
                 term=get_current_term(),
                 enroll_key='test key 1').save()
        LabGroup(course=self.course,
                 instructor=self.instructor,
                 group_name='test name 2',
                 term=get_current_term(),
                 enroll_key='test key 2').save()
        # request
        self.client.logout()
        self.client.login(username=self.student_username, password=self.password)
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        labgroups = LabGroup.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['labgroups'][0]['pk'], labgroups[0].id)
        self.assertEqual(response_body['labgroups'][0]['course'], labgroups[0].course.id)
        self.assertEqual(response_body['labgroups'][0]['instructor'], labgroups[0].instructor.id)
        self.assertEqual(response_body['labgroups'][0]['group_name'], labgroups[0].group_name)
        self.assertTrue('enroll_key' not in response_body['labgroups'][0].keys())
        self.assertEqual(response_body['labgroups'][0]['term'], labgroups[0].term)
        self.assertEqual(response_body['labgroups'][1]['pk'], labgroups[1].id)
        self.assertEqual(response_body['labgroups'][1]['course'], labgroups[1].course.id)
        self.assertEqual(response_body['labgroups'][1]['instructor'], labgroups[1].instructor.id)
        self.assertEqual(response_body['labgroups'][1]['group_name'], labgroups[1].group_name)
        self.assertTrue('enroll_key' not in response_body['labgroups'][0].keys())
        self.assertEqual(response_body['labgroups'][1]['term'], labgroups[1].term)


class LabGroupRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on LabGroupRUDView.
    """
    def setUp(self):
        # create test user with permissions
        self.instructor_username = 'instructor'
        self.student_username = 'student'
        self.password = 'test'
        self.instructor_user = User.objects.create_user(username=self.instructor_username, password=self.password)
        self.student_user = User.objects.create_user(username=self.student_username, password=self.password)
        self.instructor_user.groups.add(permissions.get_or_create_instructor_permissions())
        self.student_user.groups.add(permissions.get_or_create_student_permissions())
        self.client.login(username=self.instructor_username, password=self.password)
        # Create foreign keys
        self.instructor = Instructor(user=self.instructor_user, wwuid="1234567")
        self.instructor.save()
        self.course_1 = Course(name="test course 1")
        self.course_1.save()
        self.course_2 = Course(name="test course 2")
        self.course_2.save()
        # add labgroups to database
        self.labgroup_1 = LabGroup(course=self.course_1,
                                   instructor=self.instructor,
                                   term='test1',
                                   enroll_key='test key 1')
        self.labgroup_1.save()
        self.labgroup_2 = LabGroup(course=self.course_1,
                                   instructor=self.instructor,
                                   term='test2',
                                   enroll_key='test key 2')
        self.labgroup_2.save()
        self.labgroup_3 = LabGroup(course=self.course_1,
                                   instructor=self.instructor,
                                   term='test3',
                                   enroll_key='test key 3')
        self.labgroup_3.save()
        # retrieve the view
        self.view_name = 'api:lab-group-rud'

    def test_labgroup_retrieve_instructor(self):
        """
        Tests that a labgroup is properly retrieved for instructors.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.labgroup_2.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.labgroup_2.id)
        self.assertEqual(response_body['course'], self.labgroup_2.course.id)
        self.assertEqual(response_body['term'], self.labgroup_2.term)
        self.assertEqual(response_body['group_name'], self.labgroup_2.group_name)
        self.assertEqual(response_body['instructor'], self.labgroup_2.instructor.id)
        self.assertEqual(response_body['enroll_key'], self.labgroup_2.enroll_key)

    def test_labgroup_retrieve_student(self):
        """
        Tests that a labgroup is properly retrieved for students.
        """
        # request
        self.client.logout()
        self.client.login(username=self.student_username, password=self.password)
        response = self.client.get(reverse(self.view_name, args=[self.labgroup_2.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.labgroup_2.id)
        self.assertEqual(response_body['course'], self.labgroup_2.course.id)
        self.assertEqual(response_body['term'], self.labgroup_2.term)
        self.assertEqual(response_body['group_name'], self.labgroup_2.group_name)
        self.assertEqual(response_body['instructor'], self.labgroup_2.instructor.id)
        self.assertTrue('enroll_key' not in response_body.keys())

    def test_labgroup_update(self):
        """
        Tests that a labgroup is properly updated.
        """
        # modify values
        request_body = {
            'course': self.course_2.id,
            'instructor': self.instructor.id,
            'group_name': 'changed',
            'term': 'FALL2000',
            'enroll_key': 'changed',
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.labgroup_2.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        labgroup = LabGroup.objects.get(id=self.labgroup_2.id)
        self.assertEqual(labgroup.id, self.labgroup_2.id)
        self.assertEqual(labgroup.course.id, request_body['course'])
        self.assertEqual(labgroup.group_name, request_body['group_name'])
        self.assertEqual(labgroup.instructor.id, request_body['instructor'])
        self.assertEqual(labgroup.term, request_body['term'])
        self.assertEqual(labgroup.enroll_key, request_body['enroll_key'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.labgroup_2.id)
        self.assertEqual(response_body['course'], request_body['course'])
        self.assertEqual(response_body['group_name'], request_body['group_name'])
        self.assertEqual(response_body['instructor'], request_body['instructor'])
        self.assertEqual(response_body['term'], request_body['term'])
        self.assertEqual(response_body['enroll_key'], request_body['enroll_key'])

    def test_labgroup_destroy(self):
        """
        Tests that a labgroup is properly destroyed.
        """
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.labgroup_2.id]))
        # test database
        labgroups = LabGroup.objects.all()
        self.assertTrue(self.labgroup_1 in labgroups)
        self.assertTrue(self.labgroup_2 not in labgroups)
        self.assertTrue(self.labgroup_3 in labgroups)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


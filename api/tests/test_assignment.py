from django.conf import settings
from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from datetime import datetime, timedelta
import json
from pytz import timezone

from api.models import Course, Instructor, LabGroup, Assignment, AssignmentTemplate


class AssignmentLCTest(APITestCase):
    """
    Test cases for list and create requests on AssignmentLCView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.instructor_user = User.objects.create_user(username=self.username, password=self.password)
        self.instructor_user.user_permissions.add(Permission.objects.get(codename='add_assignment'))
        self.client.login(username=self.username, password=self.password)
        # populate test database
        self.instructor = Instructor(user=self.instructor_user, wwuid='9994141')
        self.instructor.save()
        self.course = Course(name='Bounty Hunting 101')
        self.course.save()
        self.group = LabGroup(course=self.course, instructor=self.instructor, term='before', enroll_key='4')
        self.group.save()
        self.template = AssignmentTemplate(course=self.course, name='Royalty Kidnapping Section A')
        self.template.save()
        # retrieve the view
        self.view_name = 'api:assignment-lc'

    def test_assignment_create(self):
        """
        Tests that an assignment is properly created.
        """
        # request
        request_body = {
            'assignment_template': self.template.id,
            'labgroup': self.group.id,
            'open_date': '2013-12-12T22:22:22Z',
            'close_date': '2014-12-12T22:22:22Z',
        }
        response = self.client.post(reverse(self.view_name), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        assignment = Assignment.objects.first()
        self.assertEqual(assignment.assignment_template.id, request_body['assignment_template'])
        self.assertEqual(assignment.labgroup.id, request_body['labgroup'])
        self.assertEqual(assignment.open_date.replace(tzinfo=None), datetime.strptime(request_body['open_date'], '%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(assignment.close_date.replace(tzinfo=None), datetime.strptime(request_body['close_date'], '%Y-%m-%dT%H:%M:%SZ'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['assignment_template'], request_body['assignment_template'])
        self.assertEqual(response_body['labgroup'], request_body['labgroup'])
        self.assertEqual(response_body['open_date'], request_body['open_date'])
        self.assertEqual(response_body['close_date'], request_body['close_date'])

    def test_assignment_create_template_course_incompatible(self):
        """
        Tests that an assignment is not created when the assignment template doesn't belong to a shared course.
        """
        # create different course
        course = Course(name='other course')
        course.save()
        # create different template
        template = AssignmentTemplate(course=course, name='other template')
        template.save()
        # request
        current_time = datetime.now(timezone(settings.TIME_ZONE))
        request_body = {
            'assignment_template': template.id,
            'labgroup': self.group.id,
            'open_date': (current_time - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'close_date': (current_time + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ'),
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # test database
        self.assertFalse(Assignment.objects.exists())

    def test_assignment_list(self):
        """
        Tests that assignments are properly listed.
        """
        # add assignments to database
        Assignment(assignment_template=self.template, labgroup=self.group, open_date='2013-12-12T22:22:22Z', close_date='2014-12-12T22:22:22Z').save()
        Assignment(assignment_template=self.template, labgroup=self.group, open_date='2013-12-10T22:22:22Z', close_date='2014-12-10T22:22:22Z').save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        assignments = Assignment.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['assignments'][0]['assignment_template'], assignments[0].assignment_template.id)
        self.assertEqual(response_body['assignments'][0]['name'], assignments[0].assignment_template.name)
        self.assertEqual(response_body['assignments'][0]['labgroup'], assignments[0].labgroup.id)
        self.assertEqual(datetime.strptime(response_body['assignments'][0]['open_date'], '%Y-%m-%dT%H:%M:%SZ'), assignments[0].open_date.replace(tzinfo=None))
        self.assertEqual(datetime.strptime(response_body['assignments'][0]['close_date'], '%Y-%m-%dT%H:%M:%SZ'), assignments[0].close_date.replace(tzinfo=None))
        self.assertEqual(response_body['assignments'][1]['assignment_template'], assignments[1].assignment_template.id)
        self.assertEqual(response_body['assignments'][1]['name'], assignments[1].assignment_template.name)
        self.assertEqual(response_body['assignments'][1]['labgroup'], assignments[1].labgroup.id)
        self.assertEqual(datetime.strptime(response_body['assignments'][1]['open_date'], '%Y-%m-%dT%H:%M:%SZ'), assignments[1].open_date.replace(tzinfo=None))
        self.assertEqual(datetime.strptime(response_body['assignments'][1]['close_date'], '%Y-%m-%dT%H:%M:%SZ'), assignments[1].close_date.replace(tzinfo=None))


class AssignmentRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on AssignmentRUDView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.instructor_user = User.objects.create_user(username=self.username, password=self.password)
        self.instructor_user.user_permissions.add(Permission.objects.get(codename='add_assignment'))
        self.instructor_user.user_permissions.add(Permission.objects.get(codename='change_assignment'))
        self.instructor_user.user_permissions.add(Permission.objects.get(codename='delete_assignment'))
        self.client.login(username=self.username, password=self.password)
        # populate test database
        self.instructor = Instructor(user=self.instructor_user, wwuid='9994141')
        self.instructor.save()
        self.course = Course(name='Bounty Hunting 101')
        self.course.save()
        self.group = LabGroup(course=self.course, instructor=self.instructor, term='before', enroll_key='4')
        self.group.save()
        self.template = AssignmentTemplate(course=self.course, name='Royalty Kidnapping Section A')
        self.template.save()
        self.assignment = Assignment(assignment_template=self.template, labgroup=self.group, open_date='2013-12-10T22:22:22Z', close_date='2014-12-10T22:22:22Z')
        self.assignment.save()
        self.assignment2 = Assignment(assignment_template=self.template, labgroup=self.group, open_date='2014-12-10T22:22:22Z', close_date='2015-12-10T22:22:22Z')
        self.assignment2.save()
        self.assignment3 = Assignment(assignment_template=self.template, labgroup=self.group, open_date='1492-12-10T22:22:22Z', close_date='3012-12-10T22:22:22Z')
        self.assignment3.save()
        # retrieve the view
        self.view_name = 'api:assignment-rud'

    def test_assignment_retrieve(self):
        """
        Tests that an assignment is properly retrieved.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.assignment.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['assignment_template'], self.assignment.assignment_template.id)
        self.assertEqual(response_body['name'], self.assignment.assignment_template.name)
        self.assertEqual(response_body['labgroup'], self.assignment.labgroup.id)
        self.assertEqual(response_body['open_date'], self.assignment.open_date)
        self.assertEqual(response_body['close_date'], self.assignment.close_date)

    def test_assignment_update(self):
        """
        Tests that an assignment is properly updated.
        """
        # modify values
        request_body = {
            'assignment_template': self.template.id,
            'labgroup': self.group.id,
            'open_date': '1890-10-10T22:22:22Z',
            'close_date': '1892-10-10T22:22:22Z',
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.assignment.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        assignment_tester = Assignment.objects.filter(pk=self.assignment.id).first()
        self.assertEqual(assignment_tester.assignment_template.id, request_body['assignment_template'])
        self.assertEqual(assignment_tester.labgroup.id, request_body['labgroup'])
        self.assertEqual(assignment_tester.open_date.replace(tzinfo=None), datetime.strptime(request_body['open_date'], '%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(assignment_tester.close_date.replace(tzinfo=None), datetime.strptime(request_body['close_date'], '%Y-%m-%dT%H:%M:%SZ'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['assignment_template'], request_body['assignment_template'])
        self.assertEqual(response_body['labgroup'], request_body['labgroup'])
        self.assertEqual(response_body['open_date'], request_body['open_date'])
        self.assertEqual(response_body['close_date'], request_body['close_date'])

    def test_assignment_destroy(self):
        """
        Tests that an assignment is properly destroyed.
        """
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.assignment2.id]))
        # test database
        assignments = Assignment.objects.all()
        self.assertTrue(self.assignment in assignments)
        self.assertTrue(self.assignment2 not in assignments)
        self.assertTrue(self.assignment3 in assignments)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

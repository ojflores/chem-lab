from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from datetime import datetime, timedelta
import json
from pytz import timezone

from api.models import Course, Instructor, LabGroup, Assignment, AssignmentTemplate, AssignmentEntry, Student
from api.views.view_labgroup import get_current_term


class AssignmentEntryStartTest(APITestCase):
    """
    Test cases for starting assignments on AssignmentEntryStartView.
    """

    def setUp(self):
        # create test user with permissions
        self.student_username = 'student'
        self.instructor_username = 'instructor'
        self.password = 'test'
        self.student_user = User.objects.create_user(username=self.student_username, password=self.password)
        self.instructor_user = User.objects.create_user(username=self.instructor_username, password=self.password)
        self.client.login(username=self.student_username, password=self.password)
        # populate test database
        self.instructor = Instructor(user=self.instructor_user, wwuid='9994141')
        self.instructor.save()
        self.course = Course(name='Bounty Hunting 101')
        self.course.save()
        self.group = LabGroup(course=self.course,
                              instructor=self.instructor,
                              term=get_current_term(),
                              enroll_key='4',
                              group_name='Group A')
        self.group.save()
        self.student = Student(user=self.student_user, labgroup=self.group, wwuid='1111111')
        self.student.save()
        self.template = AssignmentTemplate(course=self.course, name='Royalty Kidnapping Section A')
        self.template.save()
        self.assignment = Assignment(assignment_template=self.template,
                                     labgroup=self.group,
                                     open_date=datetime.now(timezone(settings.TIME_ZONE)),
                                     close_date=datetime.now(timezone(settings.TIME_ZONE)) + timedelta(days=1))
        self.assignment.save()
        # retrieve the view
        self.view_name = 'api:assignment-entry-start'

    def test_assignment_start(self):
        """
        Tests that an assignment is properly created.
        """
        # request
        response = self.client.post(reverse(self.view_name, args=[self.assignment.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test return code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test database
        assignment_entry = AssignmentEntry.objects.get(id=response_body['pk'])
        self.assertEqual(assignment_entry.student, self.student)
        self.assertEqual(assignment_entry.assignment, self.assignment)
        self.assertNotEqual(assignment_entry.start_date, None)
        self.assertEqual(assignment_entry.submit_date, None)
        # test response
        self.assertEqual(response_body['pk'], assignment_entry.id)
        self.assertEqual(response_body['student'], assignment_entry.student.id)
        self.assertEqual(datetime.strptime(response_body['start_date'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                         assignment_entry.start_date.replace(tzinfo=None))
        self.assertEqual(response_body['submit_date'], None)

    def test_assignment_start_duplicate(self):
        self.client.post(reverse(self.view_name, args=[self.assignment.id]))
        response = self.client.post(reverse(self.view_name, args=[self.assignment.id]))
        # test database
        self.assertEqual(len(AssignmentEntry.objects.all()), 1)
        # test response
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_assignment_does_not_exist(self):
        response = self.client.post(reverse(self.view_name, args=[0]))
        # test database
        self.assertEqual(len(AssignmentEntry.objects.all()), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_student_not_assigned_assignment(self):
        # add user to different labgroup
        new_labgroup = LabGroup(course=self.course,
                                instructor=self.instructor,
                                term=get_current_term(),
                                enroll_key='ABC',
                                group_name='Group B')
        new_labgroup.save()
        self.student.labgroup = new_labgroup
        self.student.save()
        # request
        response = self.client.post(reverse(self.view_name, args=[self.assignment.id]))
        # test database
        self.assertEqual(len(AssignmentEntry.objects.all()), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AssignmentEntryEntrySubmitTest(APITestCase):
    """
    Test cases for submitting assignment on AssignmentEntrySubmitView.
    """

    def setUp(self):
        # create test user with permissions
        self.student_username = 'student'
        self.instructor_username = 'instructor'
        self.password = 'test'
        self.student_user = User.objects.create_user(username=self.student_username, password=self.password)
        self.instructor_user = User.objects.create_user(username=self.instructor_username, password=self.password)
        self.client.login(username=self.student_username, password=self.password)
        # populate test database
        self.instructor = Instructor(user=self.instructor_user, wwuid='9994141')
        self.instructor.save()
        self.course = Course(name='Bounty Hunting 101')
        self.course.save()
        self.group = LabGroup(course=self.course,
                              instructor=self.instructor,
                              term=get_current_term(),
                              enroll_key='4',
                              group_name='Group A')
        self.group.save()
        self.student = Student(user=self.student_user, labgroup=self.group, wwuid='1111111')
        self.student.save()
        self.template = AssignmentTemplate(course=self.course, name='Royalty Kidnapping Section A')
        self.template.save()
        self.assignment = Assignment(assignment_template=self.template,
                                     labgroup=self.group,
                                     open_date=datetime.now(timezone(settings.TIME_ZONE)),
                                     close_date=datetime.now(timezone(settings.TIME_ZONE)) + timedelta(days=1))
        self.assignment.save()
        self.assignment_entry = AssignmentEntry(student=self.student, assignment=self.assignment)
        self.assignment_entry.save()
        # retrieve the view
        self.view_name = 'api:assignment-entry-submit'

    def test_assignment_entry_submit(self):
        """
        Tests that an assignment is properly submitted.
        """
        # request
        response = self.client.post(reverse(self.view_name, args=[self.assignment.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        assignment_entry = AssignmentEntry.objects.get(id=self.assignment_entry.id)
        self.assertEqual(assignment_entry.student, self.student)
        self.assertEqual(assignment_entry.assignment, self.assignment)
        self.assertNotEqual(assignment_entry.start_date, None)
        self.assertNotEqual(assignment_entry.submit_date, None)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], assignment_entry.id)
        self.assertEqual(response_body['student'], self.student.id)
        self.assertEqual(response_body['assignment'], self.assignment.id)
        self.assertTrue('start_date' in response_body.keys())
        self.assertTrue('submit_date' in response_body.keys())

    def test_assignment_does_not_exist(self):
        """
        Tests that nothing happens when the assignment does not exist.
        """
        # request
        response = self.client.post(reverse(self.view_name, args=[0]))
        # test database
        assignment_entry = AssignmentEntry.objects.get(id=self.assignment_entry.id)
        self.assertEqual(assignment_entry.submit_date, None)
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_assignment_entry_does_not_started(self):
        """
        Tests that nothing happens when the assignment entry has not been started.
        """
        # delete assignment_entry
        self.assignment_entry.delete()
        # request
        response = self.client.post(reverse(self.view_name, args=[self.assignment.id]))
        # test database
        self.assertEqual(len(AssignmentEntry.objects.all()), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

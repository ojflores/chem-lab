from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import status
from api import permissions
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
import json
from pytz import timezone
from api.models import Course, Instructor, LabGroup, Assignment, AssignmentTemplate, TaskTemplate, AssignmentEntry, \
    Student, TaskEntry


class TaskEntryLCTest(APITestCase):
    """
    Test cases for list and create requests on AssignmentLCView.
    """

    def setUp(self):
        self.instructor_username = 'instructor'
        self.student_username = 'student'
        self.password = 'test'
        self.instructor_user = User.objects.create_user(username=self.instructor_username, password=self.password)
        self.student_user = User.objects.create_user(username=self.student_username, password=self.password)
        self.instructor_user.groups.add(permissions.get_or_create_instructor_permissions())
        self.student_user.groups.add(permissions.get_or_create_student_permissions())
        self.client.login(username=self.student_username, password=self.password)
        # populate test database
        self.instructor = Instructor(user=self.instructor_user, wwuid='9994141')
        self.instructor.save()
        self.course = Course(name='Bounty Hunting 101')
        self.course.save()
        self.lab_group = LabGroup(course=self.course, instructor=self.instructor, term='before', enroll_key='4')
        self.lab_group.save()
        self.template = AssignmentTemplate(course=self.course, name='Royalty Kidnapping Section A')
        self.template.save()
        self.assignment = Assignment(assignment_template=self.template,
                                     labgroup=self.lab_group,
                                     open_date=datetime.now(timezone(settings.TIME_ZONE)),
                                     close_date=datetime.now(timezone(settings.TIME_ZONE)) + timedelta(days=1))
        self.assignment.save()
        self.task_template = TaskTemplate(assignment_template=self.template,
                                          problem_num=1,
                                          prompt='prompt',
                                          numeric_only=False)
        self.task_template.save()
        self.student = Student(user=self.student_user, labgroup=self.lab_group, wwuid='12345')
        self.student.save()
        self.assignment_entry = AssignmentEntry(student=self.student, assignment=self.assignment)
        self.assignment_entry.save()
        # retrieve the view
        self.view_name = 'api:task-entry-lc'

    def test_task_entry_create(self):
        """
        Tests that a task entry is properly created.
        """
        # request
        request_body = {
            'task_template': self.task_template.id,
            'assignment_entry': self.assignment_entry.id,
            'attempts': 2,
            'raw_input': 'input',
        }
        response = self.client.post(reverse(self.view_name, args=[self.task_template.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['task_template'], request_body['task_template'])
        self.assertEqual(response_body['assignment_entry'], request_body['assignment_entry'])
        self.assertEqual(response_body['attempts'], request_body['attempts'])
        self.assertEqual(response_body['raw_input'], request_body['raw_input'])
        # test database
        task = TaskEntry.objects.get(id=response_body['pk'])
        self.assertEqual(task.assignment_entry.id, request_body['assignment_entry'])
        self.assertEqual(task.task_template.id, request_body['task_template'])
        self.assertEqual(task.attempts, request_body['attempts'])
        self.assertEqual(task.raw_input, request_body['raw_input'])

    def test_task_entry_list(self):
        """
        Tests that Task Entries are properly listed.
        """
        # add assignments to database
        task_1 = TaskEntry(assignment_entry=self.assignment_entry,
                           task_template=self.task_template,
                           attempts=3,
                           raw_input='input')
        task_1.save()
        task_2 = TaskEntry(assignment_entry=self.assignment_entry,
                           task_template=self.task_template,
                           attempts=4,
                           raw_input='input')
        task_2.save()
        # request
        response = self.client.get(reverse(self.view_name, args=[self.task_template.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['task_entry'][0]['pk'], task_1.id)
        self.assertEqual(response_body['task_entry'][0]['task_template'], task_1.task_template.id)
        self.assertEqual(response_body['task_entry'][0]['assignment_entry'], task_1.assignment_entry.id)
        self.assertEqual(response_body['task_entry'][0]['attempts'], task_1.attempts)
        self.assertEqual(response_body['task_entry'][0]['raw_input'], task_1.raw_input)
        self.assertEqual(response_body['task_entry'][1]['pk'], task_2.id)
        self.assertEqual(response_body['task_entry'][1]['task_template'], task_2.task_template.id)
        self.assertEqual(response_body['task_entry'][1]['assignment_entry'], task_2.assignment_entry.id)
        self.assertEqual(response_body['task_entry'][1]['attempts'], task_2.attempts)
        self.assertEqual(response_body['task_entry'][1]['raw_input'], task_2.raw_input)


class TaskEntryRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on CourseRUDView.
    """

    def setUp(self):
        self.instructor_username = 'instructor'
        self.student_username = 'student'
        self.password = 'test'
        self.instructor_user = User.objects.create_user(username=self.instructor_username, password=self.password)
        self.student_user = User.objects.create_user(username=self.student_username, password=self.password)
        self.instructor_user.groups.add(permissions.get_or_create_instructor_permissions())
        self.student_user.groups.add(permissions.get_or_create_student_permissions())
        self.client.login(username=self.student_username, password=self.password)
        # populate test database
        self.instructor = Instructor(user=self.instructor_user, wwuid='9994141')
        self.instructor.save()
        self.course = Course(name='Bounty Hunting 101')
        self.course.save()
        self.lab_group = LabGroup(course=self.course, instructor=self.instructor, term='before', enroll_key='4')
        self.lab_group.save()
        self.template = AssignmentTemplate(course=self.course, name='Royalty Kidnapping Section A')
        self.template.save()
        self.assignment = Assignment(assignment_template=self.template,
                                     labgroup=self.lab_group,
                                     open_date=datetime.now(timezone(settings.TIME_ZONE)),
                                     close_date=datetime.now(timezone(settings.TIME_ZONE)) + timedelta(days=1))
        self.assignment.save()
        self.task_template = TaskTemplate(assignment_template=self.template,
                                          problem_num=1,
                                          prompt='prompt',
                                          numeric_only=False)
        self.task_template.save()
        self.task_template_2 = TaskTemplate(assignment_template=self.template,
                                            problem_num=2,
                                            prompt='prompt',
                                            numeric_only=False)
        self.task_template_2.save()
        self.student = Student(user=self.student_user, labgroup=self.lab_group, wwuid='12345')
        self.student.save()
        self.assignment_entry = AssignmentEntry(student=self.student, assignment=self.assignment)
        self.assignment_entry.save()
        self.assignment_entry_2 = AssignmentEntry(student=self.student, assignment=self.assignment)
        self.assignment_entry_2.save()
        # add tasks to the database
        self.task_1 = TaskEntry(assignment_entry=self.assignment_entry,
                                task_template=self.task_template,
                                attempts=1,
                                raw_input='input 1')
        self.task_1.save()
        self.task_2 = TaskEntry(assignment_entry=self.assignment_entry,
                                task_template=self.task_template,
                                attempts=2,
                                raw_input='input 2')
        self.task_2.save()
        self.task_3 = TaskEntry(assignment_entry=self.assignment_entry,
                                task_template=self.task_template,
                                attempts=3,
                                raw_input='input 3')
        self.task_3.save()
        # retrieve the view
        self.view_name = 'api:task-entry-rud'

    def test_task_entry_retrieve(self):
        """
        Tests that a task entry is properly retrieved.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.task_template.id, self.task_1.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.task_1.id)
        self.assertEqual(response_body['assignment_entry'], self.task_1.assignment_entry.id)
        self.assertEqual(response_body['task_template'], self.task_1.task_template.id)
        self.assertEqual(response_body['attempts'], self.task_1.attempts)
        self.assertEqual(response_body['raw_input'], self.task_1.raw_input)

    def test_task_entry_update(self):
        """
        Tests that a task entry is properly updated.
        """
        # modify values
        request_body = {
            'task_template': self.task_template.id,
            'assignment_entry': self.assignment_entry.id,
            'attempts': 10,
            'raw_input': 'new input',
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.task_template.id, self.task_2.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.task_2.id)
        self.assertEqual(response_body['task_template'], request_body['task_template'])
        self.assertEqual(response_body['assignment_entry'], request_body['assignment_entry'])
        self.assertEqual(response_body['attempts'], request_body['attempts'])
        self.assertEqual(response_body['raw_input'], request_body['raw_input'])
        # test database
        task_change = TaskEntry.objects.get(id=self.task_2.id)
        self.assertEqual(task_change.id, self.task_2.id)
        self.assertEqual(task_change.task_template.id, request_body['task_template'])
        self.assertEqual(task_change.assignment_entry.id, request_body['assignment_entry'])
        self.assertEqual(task_change.attempts, request_body['attempts'])
        self.assertEqual(task_change.raw_input, request_body['raw_input'])

    def test_task_entry_destroy(self):
        """
        Tests that a task entry is properly destroyed.
        """
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.task_template.id, self.task_2.id]))
        # test database
        task_entries = TaskEntry.objects.all()
        self.assertTrue(self.task_1 in task_entries)
        self.assertTrue(self.task_2 not in task_entries)
        self.assertTrue(self.task_3 in task_entries)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from datetime import datetime, timedelta
from pytz import timezone

from api import models
from api.views import get_current_term


class GenerateCSVTest(APITestCase):
    """
    Test cases for POST requests on EnrollView.
    """

    def setUp(self):
        # create test users
        self.instructor_username = 'instructor'
        self.password = 'test'
        student_users = []
        for s in range(0, 3):
            student_users.append(User.objects.create_user(username='student{}'.format(s), password=self.password))
        self.instructor_user = User.objects.create_user(username=self.instructor_username, password=self.password)
        self.client.login(username=self.instructor_user, password=self.password)
        # populate the database
        self.instructor = models.Instructor(user=self.instructor_user, wwuid='1234567')
        self.instructor.save()
        self.course = models.Course(name='test course')
        self.course.save()
        self.labgroup = models.LabGroup(course=self.course,
                                        instructor=self.instructor,
                                        group_name='A',
                                        term=get_current_term(),
                                        enroll_key='ABC')
        self.labgroup.save()
        students = []
        for i, student in enumerate(student_users):
            students.append(models.Student(labgroup=self.labgroup, user=student, wwuid=str(i + 1) * 7))
            students[-1].save()
        self.assignment_template = models.AssignmentTemplate(course=self.course, name='test assignment template')
        self.assignment_template.save()
        self.task_templates = []
        for task in range(1, 4):
            self.task_templates.append(models.TaskTemplate(assignment_template=self.assignment_template,
                                                           problem_num=task,
                                                           summary='test summary',
                                                           prompt='test prompt',
                                                           numeric_only=False))
            self.task_templates[-1].save()
        self.assignment = models.Assignment(assignment_template=self.assignment_template,
                                            labgroup=self.labgroup,
                                            open_date=datetime.now(timezone(settings.TIME_ZONE)),
                                            close_date=datetime.now(timezone(settings.TIME_ZONE)) + timedelta(days=1))
        self.assignment.save()
        assignment_entries = []
        for ae in range(0, 3):
            assignment_entries.append(models.AssignmentEntry(student=students[ae],
                                                             assignment=self.assignment,
                                                             start_date=datetime.now(timezone(settings.TIME_ZONE))))
            assignment_entries[-1].save()
        for ae, student in zip(assignment_entries, students):
            for tt in self.task_templates:
                models.TaskEntry(assignment_entry=ae,
                                 task_template=tt,
                                 attempts=1,
                                 raw_input='{}-{}'.format(student.wwuid, str(tt.problem_num))).save()

        # retrieve the view
        self.view_name = 'api:assignment-csv'

    def test_generate_csv(self):
        """
        Tests that a CSV is properly generated for an assignment.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.assignment.id]))
        # test response
        csv = 'student,1,2,3\r\n' \
              '1111111,1111111-1,1111111-2,1111111-3\r\n' \
              '2222222,2222222-1,2222222-2,2222222-3\r\n' \
              '3333333,3333333-1,3333333-2,3333333-3\r\n'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode('utf-8'), csv)

    def test_instructor_not_owner(self):
        """
        Tests that a CSV is not generated if an instructor does not own the assignment.
        """
        # create new instructor
        password = 'password'
        new_instructor_user = User.objects.create_user(username='new_instructor', password=password)
        new_instructor = models.Instructor(user=new_instructor_user, wwuid='8888888')
        new_instructor.save()
        self.client.logout()
        self.client.login(username=new_instructor_user.username, password=password)
        # request
        response = self.client.get(reverse(self.view_name, args=[self.assignment.id]))
        # test repsonse
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

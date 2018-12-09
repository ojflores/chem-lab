from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from datetime import datetime, timedelta
import json
from pytz import timezone

from api import permissions
from api.models import AssignmentTemplate, Course, Instructor, Student, Assignment, LabGroup
from api.views.view_labgroup import get_current_term


class AssignmentTemplateLCTest(APITestCase):
    """
    Test cases for list and create requests on AssignmentTemplateLCView.
    """

    def setUp(self):
        # create test user with permissions
        self.instructor_username = 'instructor'
        self.password = 'test'
        self.instructor_user = User.objects.create_user(username=self.instructor_username, password=self.password)
        self.instructor = Instructor(user=self.instructor_user, wwuid='9999999')
        self.instructor.save()
        group = permissions.get_or_create_instructor_permissions()
        group.user_set.add(self.instructor_user)
        self.client.login(username=self.instructor_username, password=self.password)
        # retrieve the view
        self.view_name = 'api:template-lc'

        # make a fake course
        self.course = Course(name="TestCourse")
        self.course.save()

    def test_assignment_template_create(self):
        """
        Tests that an assignment template is properly created.
        """
        # request
        request_body = {
            'name': 'test name',
            'course': self.course.id
        }
        # create assignment template
        response = self.client.post(reverse(self.view_name), request_body)
        response_body = json.loads(response.content.decode('utf-8'))

        # test database
        temp = AssignmentTemplate.objects.first()
        self.assertEqual(temp.name, request_body['name'])
        self.assertEqual(self.course.id, request_body['course'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['pk'], temp.id)
        self.assertEqual(response_body['name'], request_body['name'])
        self.assertEqual(response_body['course'], self.course.id)

    def test_assignment_template_list_instructor(self):
        """
        Tests that assignment templates are properly listed for instructors.
        """
        # add assignment templates to database

        AssignmentTemplate(name='test name 1', course=self.course).save()
        AssignmentTemplate(name='test name 2', course=self.course).save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        assignments = AssignmentTemplate.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['templates'][0]['pk'], assignments[0].id)
        self.assertEqual(response_body['templates'][0]['course'], assignments[0].course.id)
        self.assertEqual(response_body['templates'][0]['name'], assignments[0].name)
        self.assertEqual(response_body['templates'][1]['pk'], assignments[1].id)
        self.assertEqual(response_body['templates'][1]['course'], assignments[1].course.id)
        self.assertEqual(response_body['templates'][1]['name'], assignments[1].name)

    def test_assignment_template_list_student(self):
        """
        Tests that assignment templates are properly listed for students.
        """
        # create a labgroup
        labgroup_1 = LabGroup(group_name='A',
                              course=self.course,
                              instructor=self.instructor,
                              term=get_current_term(),
                              enroll_key='ABC')
        labgroup_1.save()
        # create an unused labgroup
        labgroup_2 = LabGroup(group_name='B',
                              course=self.course,
                              instructor=self.instructor,
                              term=get_current_term(),
                              enroll_key='ABC')
        labgroup_2.save()
        # create student user
        student_user = User.objects.create_user(username='student', password=self.password)
        Student(user=student_user, wwuid='1111111', labgroup=labgroup_1).save()
        group = permissions.get_or_create_student_permissions()
        group.user_set.add(student_user)
        self.client.logout()
        self.client.login(username=student_user.username, password=self.password)
        # add assignment templates to database
        at1 = AssignmentTemplate(name='test name 1', course=self.course)
        at1.save()
        at2 = AssignmentTemplate(name='test name 2', course=self.course)
        at2.save()
        # assign student the first assignment template
        assignment = Assignment(assignment_template=at1,
                                labgroup=labgroup_1,
                                open_date=datetime.now(timezone(settings.TIME_ZONE)) - timedelta(days=1),
                                close_date=datetime.now(timezone(settings.TIME_ZONE)) + timedelta(days=1))
        assignment.save()
        # create different assignment
        Assignment(assignment_template=at2,
                   labgroup=labgroup_2,
                   open_date=datetime.now(timezone(settings.TIME_ZONE)) - timedelta(days=1),
                   close_date=datetime.now(timezone(settings.TIME_ZONE)) + timedelta(days=1))
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        assignments = AssignmentTemplate.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['templates']), 1)
        self.assertEqual(response_body['templates'][0]['pk'], assignments[0].id)
        self.assertEqual(response_body['templates'][0]['course'], assignments[0].course.id)
        self.assertEqual(response_body['templates'][0]['name'], assignments[0].name)


class TemplateRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on TemplateRUDView.
    """

    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        Instructor(user=self.user, wwuid='9999999').save()
        group = permissions.get_or_create_instructor_permissions()
        group.user_set.add(self.user)
        self.client.login(username=self.username, password=self.password)
        # add courses and or templates to database
        self.course = Course(name="testcourse")
        self.course.save()
        self.template_1 = AssignmentTemplate(name='test name 1', course=self.course)
        self.template_1.save()
        self.template_2 = AssignmentTemplate(name='test name 2', course=self.course)
        self.template_2.save()
        self.template_3 = AssignmentTemplate(name='test name 3', course=self.course)
        self.template_3.save()
        # retrieve the view
        self.view_name = 'api:template-rud'

    def test_assignment_template_retrieve(self):
        """
        Tests that a assignment template is properly retrieved.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.template_2.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.template_2.id)
        self.assertEqual(response_body['name'], self.template_2.name)
        self.assertEqual(response_body['course'], self.course.id)

    def test_assignment_template_update(self):
        """
        Tests that a template is properly updated.
        """
        # modify values
        request_body = {
            'name': 'name changed',
            'course': self.course.id
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.template_2.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        assignment_template = AssignmentTemplate.objects.filter(name=request_body['name'],
                                                                course=request_body['course']).first()
        self.assertEqual(assignment_template.id, self.template_2.id)
        self.assertEqual(assignment_template.course.id, request_body['course'])
        self.assertEqual(assignment_template.name, request_body['name'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.template_2.id)
        self.assertEqual(response_body['course'], request_body['course'])
        self.assertEqual(response_body['name'], request_body['name'])

    def test_assignment_template_destroy(self):
        """
        Tests that a template is properly destroyed.
        """
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.template_2.id]))
        # test database
        assignment_templates = AssignmentTemplate.objects.all()
        self.assertTrue(self.template_1 in assignment_templates)
        self.assertTrue(self.template_2 not in assignment_templates)
        self.assertTrue(self.template_3 in assignment_templates)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from api.models import AssignmentTemplate
from api.models import Course

class AssignmentTemplateLCTest(APITestCase):
    """
    Test cases for list and create requests on CourseLCView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='add_assignmenttemplate'))
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'api:template-lc'

        #make a fake course
        course = Course(name="TestCourse")
        course.save()

        self.course = course


    def test_assignment_template_create(self):
        """
        Tests that a course is properly created.
        """
        # request
        request_body = \
        {
            'name': 'test name',
            'course': self.course.id
        }

        response = self.client.post(reverse(self.view_name), request_body)

        response_body = json.loads(response.content.decode('utf-8'))
        print(response_body)
        #create assignment template
        # test database
        temp = AssignmentTemplate.objects.first()
        self.assertEqual(temp.name, request_body['name'])
        self.assertEqual(self.course.id, request_body['course'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['pk'], temp.id)
        self.assertEqual(response_body['name'], request_body['name'])
        self.assertEqual(response_body['course'], self.course.id)

    def test_assignment_template_list(self):
        """
        Tests that courses are properly listed.
        """
        # add courses to database

        AssignmentTemplate(name='test name 1', course=self.course).save()
        AssignmentTemplate(name='test name 2', course=self.course).save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        assignments = AssignmentTemplate.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['templates'][0]['pk'], assignments[0].id)
        self.assertEqual(response_body['templates'][0]['name'], assignments[0].name)
        self.assertEqual(response_body['templates'][1]['pk'], assignments[1].id)
        self.assertEqual(response_body['templates'][1]['name'], assignments[1].name)


class CourseRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on CourseRUDView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='change_assignmenttemplate'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_assignmenttemplate'))
        self.client.login(username=self.username, password=self.password)
        # add courses to database
        self.course = Course(name="testcourse")
        self.course.save() #John added this line and is not sure about it...
        self.template_1 = AssignmentTemplate(name='test name 1',course =self.course)
        self.template_1.save()
        self.template_2 = AssignmentTemplate(name='test name 2',course =self.course)
        self.template_2.save()
        self.template_3 = AssignmentTemplate(name='test name 3',course =self.course)
        self.template_3.save()
        # retrieve the view
        self.view_name = 'api:template-rud'

    def test_template_retrieve(self):
        """
        Tests that a course is properly retrieved.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.template_2.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        print("RESPONSE BODY:")
        print(response_body)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.template_2.id)
        self.assertEqual(response_body['name'], self.template_2.name)
        self.assertEqual(response_body['course'], self.course.id)

    def test_template_update(self):
        """
        Tests that a course is properly updated.
        """
        # modify values
        request_body = {
            'name': 'name changed',
            'course' : self.course.id
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.template_2.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        # self.template_1 = AssignmentTemplate(name='test name 1',course =self.course)
        course = AssignmentTemplate.objects.filter(name=request_body['name'],course=request_body['course']).first()
        self.assertEqual(course.id, self.template_2.id)
        self.assertEqual(course.name, request_body['name'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.template_2.id)
        self.assertEqual(response_body['name'], request_body['name'])

    def test_template_destroy(self):
        """
        Tests that a course is properly destroyed.
        """
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.template_2.id]))
        # test database
        courses = AssignmentTemplate.objects.all()
        self.assertTrue(self.template_1 in courses)
        self.assertTrue(self.template_2 not in courses)
        self.assertTrue(self.template_3 in courses)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

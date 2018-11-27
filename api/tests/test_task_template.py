from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from api.models import AssignmentTemplate, TaskTemplate, Course


class TaskTemplateLCTest(APITestCase):
    """
    Test cases for list and create requests on TaskTemplateLCView.
    """

    """
    Copied from models.py:
    
    assignment_template = models.ForeignKey(AssignmentTemplate, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    summary = models.TextField(blank=True)
    prompt = models.TextField()
    prompt_format = models.CharField(max_length=50, null=True)
    image_urls = models.TextField(null=True)
    attempts_allowed = models.IntegerField(null=True)
    numeric_accuracy = models.IntegerField(null=True)
    numeric_only = models.BooleanField()
    """

    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='add_tasktemplate'))
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'api:task-template-lc'

        # make a fake course
        self.course = Course(name="TestCourse")
        self.course.save()

        # make a fake assignmnet_template
        self.assignment_template = AssignmentTemplate(course=self.course, name="TestAssignmentTemplate")
        self.assignment_template.save()

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

    def test_task_template_list(self):
        """
        Tests that task templates are properly listed.
        """
        # add task templates to database

        TaskTemplate(assignment_template=self.assignment_template,
                     name='test name 1',
                     summary='test summary 1',
                     prompt='test prompt 1',
                     prompt_format='test format 1',
                     image_urls='test image 1',
                     attempts_allowed=3,
                     numeric_accuracy=2,
                     numeric_only=False).save()
        TaskTemplate(assignment_template=self.assignment_template,
                     name='test name 2',
                     summary='test summary 2',
                     prompt='test prompt 2',
                     prompt_format='test format 2',
                     image_urls='test image 2',
                     attempts_allowed=3,
                     numeric_accuracy=2,
                     numeric_only=False).save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        task_templates = TaskTemplate.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['task_templates'][0]['pk'], task_templates[0].id)
        self.assertEqual(response_body['task_templates'][0]['assignment_template'], task_templates[0].assignment_template.id)
        self.assertEqual(response_body['task_templates'][0]['name'], task_templates[0].name)
        self.assertEqual(response_body['task_templates'][0]['summary'], task_templates[0].summary)
        self.assertEqual(response_body['task_templates'][0]['prompt'], task_templates[0].prompt)
        self.assertEqual(response_body['task_templates'][0]['prompt_format'], task_templates[0].prompt_format)
        self.assertEqual(response_body['task_templates'][0]['image_urls'], task_templates[0].image_urls)
        self.assertEqual(response_body['task_templates'][0]['attempts_allowed'], task_templates[0].attempts_allowed)
        self.assertEqual(response_body['task_templates'][0]['numeric_accuracy'], task_templates[0].numeric_accuracy)
        self.assertEqual(response_body['task_templates'][0]['numeric_only'], task_templates[0].numeric_only)
        self.assertEqual(response_body['task_templates'][1]['pk'], task_templates[0].id)
        self.assertEqual(response_body['task_templates'][1]['assignment_template'], task_templates[0].assignment_template.id)
        self.assertEqual(response_body['task_templates'][1]['name'], task_templates[0].name)
        self.assertEqual(response_body['task_templates'][1]['summary'], task_templates[0].summary)
        self.assertEqual(response_body['task_templates'][1]['prompt'], task_templates[0].prompt)
        self.assertEqual(response_body['task_templates'][1]['prompt_format'], task_templates[0].prompt_format)
        self.assertEqual(response_body['task_templates'][1]['image_urls'], task_templates[0].image_urls)
        self.assertEqual(response_body['task_templates'][1]['attempts_allowed'], task_templates[0].attempts_allowed)
        self.assertEqual(response_body['task_templates'][1]['numeric_accuracy'], task_templates[0].numeric_accuracy)
        self.assertEqual(response_body['task_templates'][1]['numeric_only'], task_templates[0].numeric_only)


class TemplateRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on TemplateRUDView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='change_assignmenttemplate'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_assignmenttemplate'))
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

    def test_template_retrieve(self):
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

    def test_template_update(self):
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
        assignment_template = AssignmentTemplate.objects.filter(name=request_body['name'], course=request_body['course']).first()
        self.assertEqual(assignment_template.id, self.template_2.id)
        self.assertEqual(assignment_template.course.id, request_body['course'])
        self.assertEqual(assignment_template.name, request_body['name'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.template_2.id)
        self.assertEqual(response_body['course'], request_body['course'])
        self.assertEqual(response_body['name'], request_body['name'])

    def test_template_destroy(self):
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

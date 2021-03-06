from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from api.models import AssignmentTemplate, TaskTemplate, Course, Instructor
from api import permissions


class TaskTemplateLCTest(APITestCase):
    """
    Test cases for list and create requests on TaskTemplateLCView.
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
        # retrieve the view
        self.view_name = 'api:task-template-lc'

        # make a fake course
        self.course = Course(name="TestCourse")
        self.course.save()

        # make a fake assignment_template
        self.assignment_template = AssignmentTemplate(course=self.course, name="TestAssignmentTemplate")
        self.assignment_template.save()

    def test_task_template_create(self):
        """
        Tests that a task template is properly created.
        """
        # request
        request_body = {
            'problem_num': 1,
            'summary': 'test summary',
            'prompt': 'test prompt',
            'prompt_format': 'test prompt format',
            'image_urls': 'test urls',
            'attempts_allowed': 3,
            'numeric_accuracy': 2,
            'numeric_only': False

        }
        # create task template
        response = self.client.post(reverse(viewname=self.view_name, args=[self.assignment_template.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))

        # test database
        temp = TaskTemplate.objects.first()
        self.assertEqual(temp.assignment_template.id, self.assignment_template.id)
        self.assertEqual(temp.problem_num, request_body['problem_num'])
        self.assertEqual(temp.summary, request_body['summary'])
        self.assertEqual(temp.prompt, request_body['prompt'])
        self.assertEqual(temp.prompt_format, request_body['prompt_format'])
        self.assertEqual(temp.image_urls, request_body['image_urls'])
        self.assertEqual(temp.attempts_allowed, request_body['attempts_allowed'])
        self.assertEqual(temp.numeric_accuracy, request_body['numeric_accuracy'])
        self.assertEqual(temp.numeric_only, request_body['numeric_only'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['assignment_template'], self.assignment_template.id)
        self.assertEqual(response_body['problem_num'], request_body['problem_num'])
        self.assertEqual(response_body['summary'], request_body['summary'])
        self.assertEqual(response_body['prompt'], request_body['prompt'])
        self.assertEqual(response_body['prompt_format'], request_body['prompt_format'])
        self.assertEqual(response_body['image_urls'], request_body['image_urls'])
        self.assertEqual(response_body['attempts_allowed'], request_body['attempts_allowed'])
        self.assertEqual(response_body['numeric_accuracy'], request_body['numeric_accuracy'])
        self.assertEqual(response_body['numeric_only'], request_body['numeric_only'])

    def test_task_template_create_include_template_key(self):
        """
        Tests that a task template is properly created even when 'assignment_template' is included in the request body.
        """
        # request
        request_body = {
            'assignment_template': 0,
            'problem_num': 1,
            'summary': 'test summary',
            'prompt': 'test prompt',
            'prompt_format': 'test prompt format',
            'image_urls': 'test urls',
            'attempts_allowed': 3,
            'numeric_accuracy': 2,
            'numeric_only': False
        }
        # create task template
        response = self.client.post(reverse(viewname=self.view_name, args=[self.assignment_template.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))

        # test database
        temp = TaskTemplate.objects.first()
        self.assertEqual(temp.assignment_template.id, self.assignment_template.id)
        self.assertEqual(temp.problem_num, request_body['problem_num'])
        self.assertEqual(temp.summary, request_body['summary'])
        self.assertEqual(temp.prompt, request_body['prompt'])
        self.assertEqual(temp.prompt_format, request_body['prompt_format'])
        self.assertEqual(temp.image_urls, request_body['image_urls'])
        self.assertEqual(temp.attempts_allowed, request_body['attempts_allowed'])
        self.assertEqual(temp.numeric_accuracy, request_body['numeric_accuracy'])
        self.assertEqual(temp.numeric_only, request_body['numeric_only'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['assignment_template'], self.assignment_template.id)
        self.assertEqual(response_body['problem_num'], request_body['problem_num'])
        self.assertEqual(response_body['summary'], request_body['summary'])
        self.assertEqual(response_body['prompt'], request_body['prompt'])
        self.assertEqual(response_body['prompt_format'], request_body['prompt_format'])
        self.assertEqual(response_body['image_urls'], request_body['image_urls'])
        self.assertEqual(response_body['attempts_allowed'], request_body['attempts_allowed'])
        self.assertEqual(response_body['numeric_accuracy'], request_body['numeric_accuracy'])
        self.assertEqual(response_body['numeric_only'], request_body['numeric_only'])

    def test_task_template_list(self):
        """
        Tests that task templates are properly listed.
        """
        # add task templates to database

        TaskTemplate(assignment_template=self.assignment_template,
                     problem_num=1,
                     summary='test summary 1',
                     prompt='test prompt 1',
                     prompt_format='test format 1',
                     image_urls='test image 1',
                     attempts_allowed=3,
                     numeric_accuracy=2,
                     numeric_only=False).save()
        TaskTemplate(assignment_template=self.assignment_template,
                     problem_num=2,
                     summary='test summary 2',
                     prompt='test prompt 2',
                     prompt_format='test format 2',
                     image_urls='test image 2',
                     attempts_allowed=3,
                     numeric_accuracy=2,
                     numeric_only=False).save()
        # request
        response = self.client.get(reverse(self.view_name, args=[self.assignment_template.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        task_templates = TaskTemplate.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['task_templates'][0]['pk'], task_templates[0].id)
        self.assertEqual(response_body['task_templates'][0]['assignment_template'], task_templates[0].assignment_template.id)
        self.assertEqual(response_body['task_templates'][0]['problem_num'], task_templates[0].problem_num)
        self.assertEqual(response_body['task_templates'][0]['summary'], task_templates[0].summary)
        self.assertEqual(response_body['task_templates'][0]['prompt'], task_templates[0].prompt)
        self.assertEqual(response_body['task_templates'][0]['prompt_format'], task_templates[0].prompt_format)
        self.assertEqual(response_body['task_templates'][0]['image_urls'], task_templates[0].image_urls)
        self.assertEqual(response_body['task_templates'][0]['attempts_allowed'], task_templates[0].attempts_allowed)
        self.assertEqual(response_body['task_templates'][0]['numeric_accuracy'], task_templates[0].numeric_accuracy)
        self.assertEqual(response_body['task_templates'][0]['numeric_only'], task_templates[0].numeric_only)
        self.assertEqual(response_body['task_templates'][1]['pk'], task_templates[1].id)
        self.assertEqual(response_body['task_templates'][1]['assignment_template'], task_templates[1].assignment_template.id)
        self.assertEqual(response_body['task_templates'][1]['problem_num'], task_templates[1].problem_num)
        self.assertEqual(response_body['task_templates'][1]['summary'], task_templates[1].summary)
        self.assertEqual(response_body['task_templates'][1]['prompt'], task_templates[1].prompt)
        self.assertEqual(response_body['task_templates'][1]['prompt_format'], task_templates[1].prompt_format)
        self.assertEqual(response_body['task_templates'][1]['image_urls'], task_templates[1].image_urls)
        self.assertEqual(response_body['task_templates'][1]['attempts_allowed'], task_templates[1].attempts_allowed)
        self.assertEqual(response_body['task_templates'][1]['numeric_accuracy'], task_templates[1].numeric_accuracy)
        self.assertEqual(response_body['task_templates'][1]['numeric_only'], task_templates[1].numeric_only)


class TaskTemplateRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on TaskTemplateRUDView.
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
        self.course = Course(name="Astrophysics 820")
        self.course.save()
        self.template = AssignmentTemplate(name='Gravitational Vortices', course=self.course)
        self.template.save()
        self.template_2 = AssignmentTemplate(name='Cosmic Drift', course=self.course)
        self.template_2.save()

        self.task_template_1 = TaskTemplate(assignment_template=self.template, problem_num=1,
                                            summary='This is a summary.', prompt='This is the prompt1',
                                            prompt_format='CAF-citation', image_urls='all', attempts_allowed=1,
                                            numeric_accuracy=1, numeric_only=False)
        self.task_template_1.save()
        self.task_template_2 = TaskTemplate(assignment_template=self.template, problem_num=2,
                                            summary='This is a summary.', prompt='This is the prompt2',
                                            prompt_format='CAF-citation', image_urls='all', attempts_allowed=2,
                                            numeric_accuracy=2, numeric_only=False)
        self.task_template_2.save()
        self.task_template_3 = TaskTemplate(assignment_template=self.template, problem_num=3,
                                            summary='This is a summary.', prompt='This is the prompt3',
                                            prompt_format='SIGFIGS', image_urls='all', attempts_allowed=3,
                                            numeric_accuracy=3, numeric_only=True)
        self.task_template_3.save()

        # retrieve the view
        self.view_name = 'api:task-template-rud'

    def test_task_template_retrieve(self):
        """
        Tests that a task template is properly retrieved.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.template_2.id, self.task_template_1.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.task_template_1.id)
        self.assertEqual(response_body['assignment_template'], self.task_template_1.assignment_template.id)
        self.assertEqual(response_body['problem_num'], self.task_template_1.problem_num)
        self.assertEqual(response_body['summary'], self.task_template_1.summary)
        self.assertEqual(response_body['prompt'], self.task_template_1.prompt)
        self.assertEqual(response_body['prompt_format'], self.task_template_1.prompt_format)
        self.assertEqual(response_body['image_urls'], self.task_template_1.image_urls)
        self.assertEqual(response_body['attempts_allowed'], self.task_template_1.attempts_allowed)
        self.assertEqual(response_body['numeric_accuracy'], self.task_template_1.numeric_accuracy)
        self.assertEqual(response_body['numeric_only'], self.task_template_1.numeric_only)

    def test_task_template_update(self):
        """
        Tests that a task template is properly updated.
        """
        # modify values
        request_body = {
            'problem_num': 10,
            'summary': 'new summary',
            'prompt': 'new prompt',
            'prompt_format': 'CAC-Citation',
            'image_urls': 'none',
            'attempts_allowed': 64,
            'numeric_accuracy': 64,
            'numeric_only': True,
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.template_2.id, self.task_template_2.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        task_template = TaskTemplate.objects.filter(problem_num=request_body['problem_num']).first()
        self.assertEqual(task_template.id, self.task_template_2.id)
        self.assertEqual(task_template.problem_num, request_body['problem_num'])
        self.assertEqual(task_template.summary, request_body['summary'])
        self.assertEqual(task_template.prompt, request_body['prompt'])
        self.assertEqual(task_template.prompt_format, request_body['prompt_format'])
        self.assertEqual(task_template.image_urls, request_body['image_urls'])
        self.assertEqual(task_template.attempts_allowed, request_body['attempts_allowed'])
        self.assertEqual(task_template.numeric_accuracy, request_body['numeric_accuracy'])
        self.assertEqual(task_template.numeric_only, request_body['numeric_only'])

        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.task_template_2.id)
        self.assertEqual(response_body['problem_num'], request_body['problem_num'])
        self.assertEqual(response_body['summary'], request_body['summary'])
        self.assertEqual(response_body['prompt'], request_body['prompt'])
        self.assertEqual(response_body['prompt_format'], request_body['prompt_format'])
        self.assertEqual(response_body['image_urls'], request_body['image_urls'])
        self.assertEqual(response_body['attempts_allowed'], request_body['attempts_allowed'])
        self.assertEqual(response_body['numeric_accuracy'], request_body['numeric_accuracy'])
        self.assertEqual(response_body['numeric_only'], request_body['numeric_only'])

    def test_task_template_destroy(self):
        """
        Tests that a task template is properly destroyed.
        """
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.template_2.id, self.task_template_2.id]))
        # test database
        task_templates = TaskTemplate.objects.all()
        self.assertTrue(self.task_template_1 in task_templates)
        self.assertTrue(self.task_template_2 not in task_templates)
        self.assertTrue(self.task_template_3 in task_templates)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

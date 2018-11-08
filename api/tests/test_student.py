from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from api.models import Student, LabGroup, Instructor, Course


class StudentLCTest(APITestCase):
    """
    Test cases for list and create requests on CourseLCView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.student_username = 'bob'
        self.instructor_user = User.objects.create_user(username=self.username, password=self.password)
        self.student_user = User.objects.create_user(username=self.student_username, password=self.password)
        self.instructor_user.user_permissions.add(Permission.objects.get(codename='add_student'))
        self.client.login(username=self.username, password=self.password)

        #populate test database
        self.instructor = Instructor(user = self.instructor_user, wwuid = '9994141')
        self.instructor.save()
        self.course = Course(name = 'fact')
        self.course.save()
        self.group = LabGroup(course = self.course, instructor = self.instructor, term = 'never', enroll_key = '6')
        self.group.save()
        # retrieve the view
        self.view_name = 'api:student-lc'

    def test_student_create(self):
        """
        Tests that a student is properly created.
        """
        # request
        request_body = {
            'user': self.student_user.id,
            'lab_group': self.group.id,
            'wwuid': '16',
        }
        response = self.client.post(reverse(self.view_name), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        student = Student.objects.first()
        self.assertEqual(student.user.id, request_body['user'])
        self.assertEqual(student.lab_group.id, request_body['lab_group'])
        self.assertEqual(student.wwuid, request_body['wwuid'])

        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['user'], student.user.id)
        self.assertEqual(response_body['lab_group'], student.lab_group.id)
        self.assertEqual(response_body['wwuid'], student.wwuid)

    def test_student_list(self):
        """
        Tests that students are properly listed.
        """
        # add students to database
        Student(user = self.student_user, lab_group = self.group, wwuid = '64').save()
        Student(user = self.instructor_user, lab_group=self.group, wwuid='12').save()

        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        students = Student.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['students'][0]['user'], students[0].user.id)
        self.assertEqual(response_body['students'][0]['lab_group'], students[0].lab_group.id)
        self.assertEqual(response_body['students'][0]['wwuid'], students[0].wwuid)
        self.assertEqual(response_body['students'][1]['user'], students[1].user.id)
        self.assertEqual(response_body['students'][1]['lab_group'], students[1].lab_group.id)
        self.assertEqual(response_body['students'][1]['wwuid'], students[1].wwuid)



class CourseRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on CourseRUDView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='change_course'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_course'))
        self.client.login(username=self.username, password=self.password)
        # add courses to database
        self.course_1 = Course(name='test name 1')
        self.course_1.save()
        self.course_2 = Course(name='test name 2')
        self.course_2.save()
        self.course_3 = Course(name='test name 3')
        self.course_3.save()
        # retrieve the view
        self.view_name = 'api:course-rud'

    def test_course_retrieve(self):
        """
        Tests that a course is properly retrieved.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.course_2.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.course_2.id)
        self.assertEqual(response_body['name'], self.course_2.name)

    def test_course_update(self):
        """
        Tests that a course is properly updated.
        """
        # modify values
        request_body = {
            'name': 'name changed',
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.course_2.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        course = Course.objects.filter(name=request_body['name']).first()
        self.assertEqual(course.id, self.course_2.id)
        self.assertEqual(course.name, request_body['name'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], self.course_2.id)
        self.assertEqual(response_body['name'], request_body['name'])

    def test_course_destroy(self):
        """
        Tests that a course is properly destroyed.
        """
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.course_2.id]))
        # test database
        courses = Course.objects.all()
        self.assertTrue(self.course_1 in courses)
        self.assertTrue(self.course_2 not in courses)
        self.assertTrue(self.course_3 in courses)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

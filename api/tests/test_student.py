from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from api.models import Course, Instructor, LabGroup, Student
from api import permissions


class StudentLCTest(APITestCase):
    """
    Test cases for list and create requests on StudentLCView.
    """
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.student_username = 'bob'
        self.instructor_user = User.objects.create_user(username=self.username, password=self.password)
        group = permissions.get_or_create_instructor_permissions()
        group.user_set.add(self.instructor_user)
        self.student_user = User.objects.create_user(username=self.student_username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # populate test database
        self.instructor = Instructor(user=self.instructor_user, wwuid='9994141')
        self.instructor.save()
        self.course = Course(name='fact')
        self.course.save()
        self.group = LabGroup(course=self.course, instructor=self.instructor, term='never', enroll_key='6')
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
            'labgroup': self.group.id,
            'wwuid': '16',
        }
        response = self.client.post(reverse(self.view_name), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        student = Student.objects.first()
        self.assertEqual(student.user.id, request_body['user'])
        self.assertEqual(student.labgroup.id, request_body['labgroup'])
        self.assertEqual(student.wwuid, request_body['wwuid'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['user'], request_body['user'])
        self.assertEqual(response_body['labgroup'], request_body['labgroup'])
        self.assertEqual(response_body['wwuid'], request_body['wwuid'])

    def test_student_permissions(self):
        """
        Tests that a student's user is assigned the appropriate permissions.
        """
        # request
        request_body = {
            'wwuid': '1111111',
            'user': self.student_user.id
        }
        self.client.post(reverse(self.view_name), request_body)
        # check that the user is in the instructor group
        self.assertTrue(self.student_user.groups.filter(name='Student').exists())

    def test_student_list(self):
        """
        Tests that students are properly listed.
        """
        # add students to database
        Student(user=self.student_user, labgroup=self.group, wwuid='64').save()
        Student(user=self.instructor_user, labgroup=self.group, wwuid='12').save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        students = Student.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['students'][0]['user'], students[0].user.id)
        self.assertEqual(response_body['students'][0]['labgroup'], students[0].labgroup.id)
        self.assertEqual(response_body['students'][0]['wwuid'], students[0].wwuid)
        self.assertEqual(response_body['students'][1]['user'], students[1].user.id)
        self.assertEqual(response_body['students'][1]['labgroup'], students[1].labgroup.id)
        self.assertEqual(response_body['students'][1]['wwuid'], students[1].wwuid)

    def test_student_list_not_shown_to_students(self):
        """
        Tests that students are not listed to other students.
        """
        # login the student
        self.client.logout()
        self.client.login(username=self.student_username, password=self.password)
        # add students to database
        Student(user=self.student_user, labgroup=self.group, wwuid='64').save()
        Student(user=self.instructor_user, labgroup=self.group, wwuid='12').save()
        # request
        response = self.client.get(reverse(self.view_name))
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StudentRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on StudentRUDView.
    """
    def setUp(self):
        # create test user with permissions and test student user
        self.instructor_username = 'test instructor'
        self.student_username_1 = 'test student 1'
        self.student_username_2 = 'test student 2'
        self.student_username_3 = 'test student 3'
        self.password = 'test'
        self.student_user_1 = User.objects.create_user(username=self.student_username_1, password=self.password)
        self.student_user_2 = User.objects.create_user(username=self.student_username_2, password=self.password)
        self.student_user_3 = User.objects.create_user(username=self.student_username_3, password=self.password)
        self.instructor_user = User.objects.create_user(username=self.instructor_username, password=self.password)
        self.instructor_user.user_permissions.add(Permission.objects.get(codename='change_student'))
        self.instructor_user.user_permissions.add(Permission.objects.get(codename='delete_student'))
        self.client.login(username=self.instructor_username, password=self.password)
        # populate database
        self.instructor = Instructor(user=self.instructor_user, wwuid='9999999')
        self.instructor.save()
        self.course = Course(name='test course')
        self.course.save()
        self.group_1 = LabGroup(course=self.course, instructor=self.instructor, term='never', enroll_key='6')
        self.group_1.save()
        self.group_2 = LabGroup(course=self.course, instructor=self.instructor, term='ever', enroll_key='8')
        self.group_2.save()
        self.student_1 = Student(user=self.student_user_1, labgroup=self.group_1, wwuid='1111111')
        self.student_1.save()
        self.student_2 = Student(user=self.student_user_2, labgroup=self.group_1, wwuid='2222222')
        self.student_2.save()
        self.student_3 = Student(user=self.student_user_3, labgroup=self.group_1, wwuid='3333333')
        self.student_3.save()
        # retrieve the view
        self.view_name = 'api:student-rud'

    def test_student_retrieve(self):
        """
        Tests that a student is properly retrieved.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.student_2.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['user'], self.student_2.user.id)
        self.assertEqual(response_body['labgroup'], self.student_2.labgroup.id)
        self.assertEqual(response_body['wwuid'], self.student_2.wwuid)

    def test_student_update(self):
        """
        Tests that a student is properly updated.
        """
        # modify values
        request_body = {
            'user': self.student_user_2.id,
            'labgroup': self.group_2.id,
            'wwuid': '8888888',
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.student_2.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        student = Student.objects.filter(user=self.student_user_2).first()
        self.assertEqual(student.user.id, request_body['user'])
        self.assertEqual(student.labgroup.id, request_body['labgroup'])
        self.assertEqual(student.wwuid, request_body['wwuid'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['user'], request_body['user'])
        self.assertEqual(response_body['labgroup'], request_body['labgroup'])
        self.assertEqual(response_body['wwuid'], request_body['wwuid'])

    def test_student_destroy(self):
        """
        Tests that a student is properly destroyed.
        """
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.student_2.id]))
        # test database
        students = Student.objects.all()
        self.assertTrue(self.student_1 in students)
        self.assertTrue(self.student_2 not in students)
        self.assertTrue(self.student_3 in students)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

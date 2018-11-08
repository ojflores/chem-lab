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
        # populate test database
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



class StudentRUDTest(APITestCase):
    """
    Test cases for retrieve, update, and destroy requests on StudentRUDView.
    """
    def setUp(self):
        # create test user with permissions and test student user
        self.instructor_username = 'test2'
        self.student_username = 'test3'
        self.password = 'test2'
        self.student_user = User.objects.create_user(username=self.student_username, password=self.password)
        self.instructor_user = User.objects.create_user(username=self.instructor_username, password=self.password)
        self.instructor_user.user_permissions.add(Permission.objects.get(codename='change_student'))
        self.instructor_user.user_permissions.add(Permission.objects.get(codename='delete_student'))
        self.client.login(username=self.instructor_username, password=self.password)
        # populate database
        self.instructor = Instructor(user=self.instructor_user, wwuid='9994141')
        self.instructor.save()
        self.course = Course(name='Encom')
        self.course.save()
        self.group = LabGroup(course=self.course, instructor=self.instructor, term='never', enroll_key='6')
        self.group.save()
        self.group_2 = LabGroup(course=self.course, instructor=self.instructor, term='ever', enroll_key='8')
        self.group_2.save()
        self.student = Student(user=self.student_user, lab_group=self.group, wwuid='694')
        self.student.save()

        # retrieve the view
        self.view_name = 'api:student-rud'

    def test_student_retrieve(self):
        """
        Tests that a student is properly retrieved.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[self.student.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['user'], self.student.user.id)
        self.assertEqual(response_body['lab_group'], self.student.lab_group.id)
        self.assertEqual(response_body['wwuid'], self.student.wwuid)

    def test_student_update(self):
        """
        Tests that a student is properly updated.
        """
        # modify values
        request_body = {
            'user': self.student_user.id,
            'lab_group': self.group_2.id,
            'wwuid': '1993',
        }
        # request
        response = self.client.put(reverse(self.view_name, args=[self.student.id]), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        student = Student.objects.filter(user=self.student_user).first()
        self.assertEqual(student.user.id, request_body['user'])
        self.assertEqual(student.lab_group.id, request_body['lab_group'])
        self.assertEqual(student.wwuid, request_body['wwuid'])
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['user'], self.student.user.id)
        self.assertEqual(response_body['user'], request_body['user'])
        self.assertEqual(response_body['lab_group'], self.group_2.id)
        self.assertEqual(response_body['lab_group'], request_body['lab_group'])
        self.assertEqual(response_body['wwuid'], '1993')
        self.assertEqual(response_body['wwuid'], request_body['wwuid'])

    def test_student_destroy(self):
        """
        Tests that a student is properly destroyed.
        """
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.student.id]))
        # test database
        students = Student.objects.all()
        self.assertTrue(self.student not in students)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

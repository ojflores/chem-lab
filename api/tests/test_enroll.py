from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import Course, Instructor, LabGroup, Student


class EnrollTest(APITestCase):
    """
    Test cases for POST requests on EnrollView.
    """

    def setUp(self):
        # create test users
        self.student_username = 'student'
        self.teacher_username = 'teacher'
        self.password = 'test'
        self.student_user = User.objects.create_user(username=self.student_username, password=self.password)
        self.instructor_user = User.objects.create_user(username=self.teacher_username, password=self.password)
        self.client.login(username=self.student_username, password=self.password)
        # populate the database
        self.student = Student(labgroup=None, user=self.student_user, wwuid='1111111')
        self.student.save()
        self.instructor = Instructor(user=self.instructor_user, wwuid='2222222')
        self.instructor.save()
        self.course = Course(name='test name')
        self.course.save()
        self.labgroup = LabGroup(course=self.course,
                                 instructor=self.instructor,
                                 group_name='A',
                                 term='FALL2018',
                                 enroll_key='ABC')
        self.labgroup.save()
        # retrieve the view
        self.view_name = 'api:enroll'

    def test_enroll(self):
        """
        Tests that a labgroup can be properly enrolled in.
        """
        # request
        request_body = {
            'wwuid': self.student.wwuid,
            'labgroup': self.labgroup.id,
            'enroll_key': self.labgroup.enroll_key
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # test database
        self.assertEqual(Student.objects.first().user, self.student_user)
        self.assertEqual(Student.objects.first().labgroup, self.labgroup)
        self.assertEqual(Student.objects.first().wwuid, self.student.wwuid)

    def test_enroll_not_student(self):
        """
        Tests that non-students cannot enroll in labgroups.
        """
        # request
        self.client.logout()
        self.client.login(username=self.teacher_username, password=self.password)
        request_body = {
            'wwuid': '2222222',
            'labgroup': self.labgroup.id,
            'enroll_key': self.labgroup.enroll_key
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # test database
        self.assertEqual(Student.objects.get(user=self.instructor_user).labgroup, self.labgroup)

    def test_enroll_bad_labgroup(self):
        """
        Tests that entering a bad labgroup is properly handled.
        """
        # request
        request_body = {
            'wwuid': self.student.wwuid,
            'labgroup': 0,
            'enroll_key': self.labgroup.enroll_key
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # test database
        self.assertEqual(Student.objects.first().labgroup, None)

    def test_enroll_bad_key(self):
        """
        Tests that a labgroup is not enrolled in with a bad key.
        """
        # request
        request_body = {
            'wwuid': self.student.wwuid,
            'labgroup': self.labgroup.id,
            'enroll_key': ''
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # test database
        self.assertEqual(Student.objects.first().labgroup, None)

    def test_missing_parameters(self):
        """
        Tests that a missing parameter causes the request to do nothing.
        """
        # request
        request_body = {
            'wwuid': self.student.wwuid,
            'enroll_key': self.labgroup.enroll_key
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # test database
        self.assertEqual(Student.objects.first().labgroup, None)

    def test_invalid_student(self):
        """
        Tests that entering invalid student does nothing.
        """
        # request
        request_body = {
            'wwuid': '123456789',  # too long
            'labgroup': self.labgroup.id,
            'enroll_key': self.labgroup.enroll_key
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # test database
        self.assertEqual(len(Student.objects.all()), 0)

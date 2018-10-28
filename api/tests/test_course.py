from django.contrib.auth.models import Permission, User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import Course


class TestCourseLCPost(APITestCase):
    '''
    Test cases for POST requests on CourseLCView.
    '''
    def setUp(self):
        # create test user with permissions
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(Permission.objects.get(codename='add_course'))
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'api:course-lc'


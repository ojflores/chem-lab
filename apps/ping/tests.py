from django.test import TestCase


class Ping(TestCase):
    """
    Test cases for '/ping'.
    """
    def test_ping_get(self):
        response = self.client.get('/ping', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), '{"result":"pong!"}')

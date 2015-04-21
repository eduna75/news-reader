__author__ = 'justus'

from app import app
import unittest


class FlaskTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_config_login(self):
        tester = app.test_client(self)
        response = tester.get('/config_login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/config_login', content_type='html/text')
        self.assertTrue(b'This is where you login!' in response.data)

    def test_login_correct(self):
        tester = app.test_client(self)
        response = tester.post('/config_login', data=dict(username='admin', password='admin'), follow_redirects=True)
        self.assertIn(b'You are now logged in!', response.data)

    def test_login_incorrect(self):
        tester = app.test_client(self)
        response = tester.post('/config_login', data=dict(username='xxx', password='xxx'), follow_redirects=True)
        self.assertIn(b'You shall not pass!', response.data)

    def test_login_correct_index(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(username='admin', password='admin'), follow_redirects=True)
        self.assertIn(b'You are now logged in!', response.data)

    def test_logout_correct(self):
        tester = app.test_client(self)
        tester.post('/config_login', data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You are logged out!', response.data)

    def test_login_required_main(self):
        tester = app.test_client(self)
        response = tester.get('/config', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    def test_login_required_logout(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)


if __name__ == "__main__":
    unittest.main()
"""
Tests for the low-Level object to access the i-doit JSON-RPC API.
"""

import configparser
import unittest

from idoitapi.API import API
import idoitapi.APIException


class TestApiObject(unittest.TestCase):
    def test_is_object(self):
        """
        Test the API constructor
        """
        obj = API(url='http://localhost', key='abc123')
        self.assertTrue(isinstance(obj, API), msg='Not an API object')
        self.assertEqual(obj.url, 'http://localhost/src/jsonrpc.php', msg='url failed')
        self.assertEqual(obj.key, 'abc123', msg='key failed')

    def test_check_url(self):
        """
        Failure tests for the API constructor's URL parameter
        """
        # Empty URL is an invalid parameter
        with self.assertRaises(idoitapi.APIException.InvalidParams):
            API(url='', key='abc123')
        # Empty API key is an invalid parameter
        with self.assertRaises(idoitapi.APIException.InvalidParams):
            API(url='http://localhost', key='')


class TestApiConnection(unittest.TestCase):

    def setUp(self):
        cp = configparser.ConfigParser(interpolation=None)
        cp.read('.config')
        self.config = cp[cp.default_section]
        self.assertNotEqual(self.config['api_key'], '-invalid-', 'Please enter the demo API key in .config')
        self.api = API(
            url=self.config['url'],
            key=self.config['api_key'],
            language=self.config['language'],
        )
        self.assertIsInstance(self.api, API, 'object is not an API instance')

    def tearDown(self):
        if self.api:
            if self.api.is_logged_in():
                self.api.logout()

    def test_login(self):
        """
        Test login()
        """
        self.api.login(
            username=self.config['username'],
            password=self.config['password'],
        )
        self.assertTrue(self.api.is_logged_in(), 'not logged in')

    def test_login_failure(self):
        """
        Failure tests for login()
        """
        with self.assertRaises(idoitapi.APIException.JSONRPC):
            self.api.login(username='test', password='')
            self.api.login(username='', password='test')


if __name__ == '__main__':
    unittest.main()

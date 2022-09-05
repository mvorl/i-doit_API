"""
Tests for requests for API namespace 'idoit'
"""

import configparser
import unittest

from idoitapi.API import API
from idoitapi.Idoit import Idoit


class TestIdoit(unittest.TestCase):
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
        self.api.login(
            username=self.config['username'],
            password=self.config['password'],
        )

    def tearDown(self):
        if self.api:
            if self.api.is_logged_in():
                self.api.logout()

    def test_read_version(self):
        """
        Test read_version()
        """
        result = Idoit(self.api).read_version()
        self.assertIsInstance(result, dict, 'version information is not a dict')

    def test_get_addons(self):
        """
        Test get_addons()
        """
        result = Idoit(self.api).get_addons()
        self.assertIsInstance(result, list, 'addons information is not a list')
        api_addon = next((el for el in result if el['title'] == 'Api'), None)
        self.assertIsNotNone(api_addon, 'No api addon found')

    def test_get_license(self):
        result = Idoit(self.api).get_license()
        self.assertIsInstance(result, dict, 'license information is not a dict')

    def test_read_constants(self):
        result = Idoit(self.api).read_constants()
        self.assertIsInstance(result, dict, 'list of constants is not a dict')

    def test_search(self):
        result = Idoit(self.api).search('admin')
        self.assertIsInstance(result, list, 'search information is not a list')


if __name__ == '__main__':
    unittest.main()

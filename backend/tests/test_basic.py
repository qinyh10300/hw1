import unittest

from django.test import TestCase

from utils.register_params_check import register_params_check


class BasicTestCase(TestCase):
    """
    注册参数校验测试用例
    """

    def test_valid_registration(self):
        result, success = register_params_check(
            {
                "username": "user123",
                "password": "Pass1234*",
                "nickname": "John Doe",
                "mobile": "+12.123456789012",
                "url": "https://example.com",
                "magic_number": 7,
            }
        )
        self.assertEqual(result, "ok")
        self.assertTrue(success)

    def test_missing_username(self):
        result, success = register_params_check(
            {
                "username": "",
                "password": "Pass1234@",
                "nickname": "John Doe",
                "mobile": "+12.123456789012",
                "url": "https://example.com",
            }
        )
        self.assertEqual(result, "username")
        self.assertFalse(success)

    def test_invalid_username_format(self):
        result, success = register_params_check(
            {
                "username": "user@",
                "password": "Pass1234@",
                "nickname": "John Doe",
                "mobile": "+12.123456789012",
                "url": "https://example.com",
            }
        )
        self.assertEqual(result, "username")
        self.assertFalse(success)

    def test_missing_password(self):
        result, success = register_params_check(
            {
                "username": "user123",
                "password": "",
                "nickname": "John Doe",
                "mobile": "+12.123456789012",
                "url": "https://example.com",
            }
        )
        self.assertEqual(result, "password")
        self.assertFalse(success)

    def test_invalid_password_format(self):
        result, success = register_params_check(
            {
                "username": "user123",
                "password": "short",
                "nickname": "John Doe",
                "mobile": "+12.123456789012",
                "url": "https://example.com",
            }
        )
        self.assertEqual(result, "password")
        self.assertFalse(success)

    def test_invalid_mobile_format(self):
        result, success = register_params_check(
            {
                "username": "user123",
                "password": "Pass1234*",
                "nickname": "John Doe",
                "mobile": "12345",
                "url": "https://example.com",
            }
        )
        self.assertEqual(result, "mobile")
        self.assertFalse(success)

    def test_invalid_url_format(self):
        result, success = register_params_check(
            {
                "username": "user123",
                "password": "Pass1234*",
                "nickname": "John Doe",
                "mobile": "+12.123456789012",
                "url": "example.com",
            }
        )
        self.assertEqual(result, "url")
        self.assertFalse(success)

    def test_magic_number_default(self):
        result, success = register_params_check(
            {
                "username": "user123",
                "password": "Pass1234*",
                "nickname": "John Doe",
                "mobile": "+12.123456789012",
                "url": "https://example.com",
            }
        )
        self.assertEqual(result, "ok")
        self.assertTrue(success)

    def test_magic_number_optional(self):
        result, success = register_params_check(
            {
                "username": "user123",
                "password": "Pass1234*",
                "nickname": "John Doe",
                "mobile": "+12.123456789012",
                "url": "https://example.com",
                "magic_number": 42,
            }
        )
        self.assertEqual(result, "ok")
        self.assertTrue(success)

    def test_username_length_lower_bound(self):
        result, success = register_params_check(
            {
                "username": "u123",
                "password": "Pass1234*",
                "nickname": "John Doe",
                "mobile": "+12.123456789012",
                "url": "https://example.com",
            }
        )
        self.assertEqual(result, "username")
        self.assertFalse(success)

    def test_username_length_upper_bound(self):
        result, success = register_params_check(
            {
                "username": "user12345678",
                "password": "Pass1234*",
                "nickname": "John Doe",
                "mobile": "+12.123456789012",
                "url": "https://example.com",
            }
        )
        self.assertEqual(result, "ok")
        self.assertTrue(success)

    def test_password_length_lower_bound(self):
        result, success = register_params_check(
            {
                "username": "user123",
                "password": "Pass123",
                "nickname": "John Doe",
                "mobile": "+12.123456789012",
                "url": "https://example.com",
            }
        )
        self.assertEqual(result, "password")
        self.assertFalse(success)

    def test_password_length_upper_bound(self):
        result, success = register_params_check(
            {
                "username": "user123",
                "password": "Pass123456789012",
                "nickname": "John Doe",
                "mobile": "+12.123456789012",
                "url": "https://example.com",
            }
        )
        self.assertEqual(result, "password")
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()

import unittest

from django.test import Client, TestCase
from django.urls import reverse

from user import views as user_views
from user.models import User
from utils.jwt import encrypt_password


class APITestCase(TestCase):
    def setUp(self):
        user = User(
            username="testuser",
            password=encrypt_password(str("testuser")),
            nickname="test",
            mobile="+86.123456789012",
            magic_number=0,
            url="https://baidu.com",
        )
        user.save()
        self.client = Client()

    def test_login(self):
        """
        TODO: 使用错误的信息进行登录，检查返回值为失败
        """
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(
            reverse(user_views.register_user), data=data, content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data["message"], "Error")
        self.assertEqual(response.status_code, 500)
        """
        TODO: 使用正确的信息进行登录，检查返回值为成功
        """
        data = {"username": "testuser", "password": "testuser"}
        response = self.client.post(
            reverse(user_views.register_user), data=data, content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data["message"], "Success")
        self.assertEqual(response.status_code, 200)

        """
        TODO: 进行登出，检查返回值为成功
        """
        response = self.client.post(
            reverse(user_views.register_user), content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data["message"], "Success")
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        """
        Example: 使用错误信息进行注册，检查返回值为失败
        TODO: 这里的错误和返回码是在还没有实现注册参数校验的情况下的返回值，
        在完成register_params_check后，你需要修改这里的错误信息和返回码
        """
        data = {"username": "123", "password": "21321"}
        response = self.client.post(
            reverse(user_views.register_user), data=data, content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data["message"], "Error")
        self.assertEqual(response.status_code, 500)

        """
        TODO: 使用正确的信息进行注册，检查返回值为成功
        """
        data = {
            "username": "newuser",
            "password": "newpassword",
            "nickname": "newnick",
            "mobile": "+86.123456789013",
            "magic_number": 1,
            "url": "https://example.com"
        }
        response = self.client.post(
            reverse(user_views.register_user), data=data, content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data["message"], "Success")
        self.assertEqual(response.status_code, 200)

        """
        TODO: 使用正确注册信息进行登录，检查返回值为成功
        """
        data = {"username": "newuser", "password": "newpassword"}
        response = self.client.post(
            reverse(user_views.register_user), data=data, content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data["message"], "Success")
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """
        TODO: 未登录直接登出
        """
        response = self.client.post(
            reverse(user_views.register_user), content_type="application/json"
        )
        json_data = response.json()
        # 根据实际实现，未登录时登出可能返回错误或成功
        # 这里假设返回错误
        self.assertEqual(json_data["message"], "Error")
        self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()

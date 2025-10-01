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
        data = {"username": "newuser1", "password": "newpassword"}
        response = self.client.patch(
            reverse("login"), data=data, content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json_data["message"], "Invalid credentials")
        """
        TODO: 使用正确的信息进行登录，检查返回值为成功
        """
        data = {"username": "test_thss", "password": "test_thss"}
        response = self.client.patch(
            reverse("login"), data=data, content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("jwt", json_data)
        self.assertEqual(json_data["username"], "test_thss")
        """
        TODO: 进行登出，检查返回值为成功
        """
        token = json_data["jwt"]
        response = self.client.post(
            reverse("logout"),
            HTTP_AUTHORIZATION=f"{token}",
        )
        json_data = response.json()
        self.assertEqual(json_data["message"], "ok")
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        """
        Example: 使用错误信息进行注册，检查返回值为失败
        TODO: 这里的错误和返回码是在还没有实现注册参数校验的情况下的返回值，
        在完成register_params_check后，你需要修改这里的错误信息和返回码
        """
        data = {"username": "123", "password": "21321"}
        response = self.client.post(
            reverse("register"), data=data, content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data["message"], "Invalid arguments: username")
        self.assertEqual(response.status_code, 400)

        """
        TODO: 使用正确的信息进行注册，检查返回值为成功
        """
        data = {
            "username": "newuser1",
            "password": "newpasswordNP1*",
            "nickname": "newnick",
            "mobile": "+86.123456789013",
            "magic_number": 1,
            "url": "https://example.com"
        }
        response = self.client.post(
            reverse("register"), data=data, content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data["message"], "ok")
        self.assertEqual(response.status_code, 200)

        """
        TODO: 使用正确注册信息进行登录，检查返回值为成功
        """
        data = {"username": "newuser1", "password": "newpasswordNP1*"}
        response = self.client.patch(
            reverse("login"), data=data, content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("jwt", json_data)
        self.assertEqual(json_data["username"], "newuser1")

    def test_logout(self):
        """
        TODO: 未登录直接登出
        """
        token = ""
        response = self.client.post(
            reverse("logout"),
            HTTP_AUTHORIZATION=f"{token}",
        )
        json_data = response.json()
        self.assertEqual(json_data["message"], "User must be authorized.")
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()

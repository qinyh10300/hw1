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
        """
        TODO: 使用正确的信息进行登录，检查返回值为成功
        """
        """
        TODO: 进行登出，检查返回值为成功
        """

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
        # print(json_data["message"], response.status_code)
        self.assertEqual(json_data["message"], "username")
        self.assertEqual(response.status_code, 400)
        """
        TODO: 使用正确的信息进行注册，检查返回值为成功
        """
        """
        TODO: 使用正确注册信息进行登录，检查返回值为成功
        """
        data = {"username": "testuser", "password": "testuser"}  # 这里使用之前创建的用户
        response = self.client.post(
            reverse(user_views.login_user), data=data, content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data["message"], "Login successful")  # 登录成功返回信息
        self.assertEqual(response.status_code, 200)  # 登录成功返回 200

    def test_logout(self):
        """
        TODO: 未登录直接登出
        """


if __name__ == "__main__":
    unittest.main()

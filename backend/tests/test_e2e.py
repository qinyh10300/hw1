import platform
import subprocess
import time
import unittest

from django.core.management import call_command
from django.test import LiveServerTestCase, override_settings
from selenium import webdriver

from app.settings import BASE_DIR
from user.controllers import create_user
from utils.jwt import encrypt_password
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


DRIVER_PATH = "drivers/chromedriver"
FRONTEND_PATH = str(BASE_DIR.parent) + "/frontend"
# cli = sys.modules['flask.cli']
# cli.show_server_banner = lambda *x: None
#
#
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)


@override_settings(
    CORS_ORIGIN_ALLOW_ALL=True,
    CORS_ALLOW_CREDENTIALS=True,
    CORS_ORIGIN_WHITELIST=["*"],
)
class SeleniumTestCase(LiveServerTestCase):
    port = 8000  # 服务器端口，默认为随机分配一个空闲端口

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # start Chrome
        options = webdriver.ChromeOptions()
        if platform.system() == "Windows":
            options.binary_location = (
                r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            )
        elif platform.system() == "Linux":
            options.binary_location = "/usr/bin/google-chrome"
        elif platform.system() == "Darwin":
            options.binary_location = (
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            )
        else:
            raise Exception("Unknown OS")
        # options.add_argument('headless')
        # You need to change this to your actual binary path.
        # You need to change this to your actual web driver path.
        cls.webclient = webdriver.Chrome(service=Service(DRIVER_PATH),options=options)
        # delete all data in the database
        call_command("flush", "--noinput")
        create_user(
            username="test_thss",
            password=encrypt_password(str("test_thss")),
            nickname="test_thss",
            url="https://baidu.com",
            mobile="+86.123456789012",
            magic_number=0,
        )

        # start the frontend server in a process
        # You need to change this to your actual frontend path.
        frontend_path = FRONTEND_PATH
        cls.frontend_process = subprocess.Popen(
            "npm run startwithoutbrowser", shell=True, cwd=frontend_path
        )

        # give the server 25 seconds to ensure it is up
        time.sleep(25)

    @classmethod
    def tearDownClass(cls):
        cls.webclient.close()
        cls.webclient.quit()
        cls.frontend_process.terminate()
        cls.frontend_process.kill()
        call_command("flush", "--noinput")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_web(self):
        """
        EXAMPLE: 使用测试用户进行登录
        """
        self.webclient.get("http://127.0.0.1:3001")
        time.sleep(1)
        self.webclient.find_element(By.XPATH, "//*[@id='root']/div/div[3]/div/a").click()
        time.sleep(1)
        self.webclient.find_element(By.ID,"username").send_keys("test_thss")
        time.sleep(1)
        self.webclient.find_element(By.ID,"password").send_keys("test_thss")
        time.sleep(1)
        self.webclient.find_element(By.XPATH,'//*[@id="root"]/div/div[3]/div/button').click()
        time.sleep(3)

        """
        TODO: 登录后发帖，发帖标题为：“Hello World”（不包括引号，下同），发帖内容为：“你好！”
        """

        """
        TODO: 更新帖子标题为：“Hello World!”（注意中英文符号），帖子内容为：“你好。”
        """

        """
        TODO: 回复刚才的帖子，回复内容为：“你好！”
        """

        """
        TODO: 退出登录
        """


if __name__ == "__main__":
    unittest.main()

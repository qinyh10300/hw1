"""
This file is used to test the installation of the Selenium WebDriver for Chrome.
When executed, it will open a Chrome window, navigate to the Baidu homepage, search for the term "软件工程" (software engineering), and then close the window.
This script is intended to verify that the WebDriver is installed correctly and that the Chrome browser can be controlled programmatically using Selenium.
To run this script, ensure that the ChromeDriver executable is installed and located in the 'drivers' directory.

Example usage:
    python driver.py

"""

import platform
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = Options()
# options.add_argument('headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# You need to change this to your actual binary path.
# options.binary_location = "C:\\Program Files\\Google\\Chrome Dev\\Application\\chrome.exe" # noqa: E501
# You need to change this to your actual web driver path.
if platform.system() == "Windows":
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
elif platform.system() == "Linux":
    options.binary_location = "/usr/bin/google-chrome"
elif platform.system() == "Darwin":
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
else:
    raise Exception("Unknown OS")
service = Service("drivers/chromedriver")
driver = webdriver.Chrome(service=service, options=options)
driver.get("http://www.baidu.com")
assert "百度" in driver.title
elem = driver.find_element(By.NAME, "wd")
elem.clear()
elem.send_keys("软件工程")
elem.send_keys(Keys.RETURN)
time.sleep(10)
driver.close()

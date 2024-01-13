import os
import socket
import time

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import browser
from dotenv import load_dotenv

from utils import attach

DEFAULT_BROWSER_VERSION = "118.0"


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='119.0'
    )


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    options = Options()

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    # browser_version = request.config.getoption('--browser_version')
    # browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    #options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": '100.0',
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    url = os.getenv('URL')

    driver = webdriver.Remote(
        #command_executor=f'http://{url}/wd/hub',
        command_executor=f"https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options
    )
    browser.config.driver = driver
    browser.config.timeout = 20
    browser.config.window_height = 1200
    browser.config.window_width = 1900
    yield browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()




@pytest.fixture(scope='function', autouse=True)
def open_browser(setup_browser):
    browser.open('https://okko.tv/')
    #time.sleep(10)
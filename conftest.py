import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time, datetime
import ssl


logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

ssl._create_default_https_context = ssl._create_unverified_context

@pytest.fixture(scope="function")
def driver_fixture(request):
    # This is setup part
    options = Options()
    options.add_experimental_option("detach", False)
    options.add_argument("--mute-audio")
    options.add_argument("--auto-play-policy=no-user-gesture-required")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    # This is teardown part
    driver.quit()
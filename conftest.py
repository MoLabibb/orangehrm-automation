# conftest.py

import sys
import os
import time
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

logging.getLogger("WDM").setLevel(logging.ERROR)

from api.candidates_api import CandidatesAPI
from pages.login_page import LoginPage


def _create_chrome_driver() -> webdriver.Chrome:

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def _create_headless_chrome_driver() -> webdriver.Chrome:

    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def pytest_configure(config):

    config._metadata = {
        "Project": "OrangeHRM Test Automation",
        "Application URL": "https://opensource-demo.orangehrmlive.com/",
        "Browser": "Google Chrome",
        "Test Types": "UI (Selenium) + API (Requests)",
        "Framework": "Pytest + Page Object Model",
        "Python Version": "3.12",
    }


def pytest_html_report_title(report):

    report.title = "OrangeHRM Automation Test Report"

    
@pytest.fixture
def driver():

    chrome_driver = _create_chrome_driver()
    chrome_driver.get("https://opensource-demo.orangehrmlive.com/")
    yield chrome_driver
    chrome_driver.quit()


@pytest.fixture(scope="class")
def api_client():


    print("\nAuthenticating API session (background)...")

    MAX_RETRIES = 3

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        auth_driver = None
        try:
            if attempt > 1:
                print(f"🔄 Retry attempt {attempt}/{MAX_RETRIES}...")
                time.sleep(3)
            auth_driver = _create_headless_chrome_driver()
            auth_driver.get("https://opensource-demo.orangehrmlive.com/")
            login_page = LoginPage(auth_driver)
            login_page.login("Admin", "admin123")
            time.sleep(3)
            WebDriverWait(auth_driver, 10).until(
                lambda d: any(c["name"] == "orangehrm" for c in d.get_cookies()),
                message="Session cookie 'orangehrm' not found after login"
            )

            client = CandidatesAPI()
            client.login_with_browser_session(auth_driver)

            print(f"✅ API session authenticated (attempt {attempt}) ✓")
            break

        except ConnectionError as e:
            last_error = e
            print(f"⚠️  Attempt {attempt} failed: {e}")

            if attempt == MAX_RETRIES:
                raise ConnectionError(
                    f"API authentication failed after {MAX_RETRIES} attempts. "
                    f"Last error: {last_error}"
                )

        finally:
            if auth_driver:
                auth_driver.quit()

    print("✅ API session ready (no browser needed for actual tests)\n")
    yield client



import sys
import unittest
import json
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class TestSuiteForBrowserStack(unittest.TestCase):

    base_url = "https://www.browserstack.com/blbalbal"
    users_sign_in_page_url = "/users/sign_in"
    user_validation_error_xpath = "//span[@aria-live='polite']"

    def setUp(self):
        self.credentials = self.get_credentials_from_json()
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    @staticmethod
    def get_credentials_from_json(creds_path="./credentials.json"):
        with open(creds_path, "r") as creds_file:
            return json.load(creds_file)

    def test_user_should_able_to_log_in(self):
        self.driver.get(f"{self.base_url}{self.users_sign_in_page_url}")
        WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located((
            By.ID, 'user_submit')))
        self.driver.find_element(By.ID, 'user_email_login').send_keys(self.credentials["invalid_email"])
        self.driver.find_element(By.ID, 'user_password').send_keys(self.credentials["password"])
        self.driver.find_element(By.ID, 'user_submit').click()
        user_validation_error_text = self.driver.find_element(By.XPATH, self.user_validation_error_xpath).text
        self.assertEqual(user_validation_error_text, "Invalid Email", f"Email validation error not shown!")
        self.assertIn(self.users_sign_in_page_url, self.driver.current_url, f"Not on sign in page!")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--base-page-url":
        TestSuiteForBrowserStack.base_url = sys.argv[2]
        sys.argv = sys.argv[:1]
    unittest.main()

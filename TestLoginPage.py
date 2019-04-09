# -*- coding: utf-8 -*-

import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class TestLoginPage(unittest.TestCase):
    """
    This class cover the test cases related to login page
    """
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://frontend.qa.entera.ai/signin"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.driver.maximize_window()
        self.driver.get(self.base_url)

    def test_login_with_valid_credentials(self):
        """
        Verify user should be able to login with valid credential and it should take user to dashboard page
        """
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
        driver.find_element_by_css_selector('input[name="username"]').clear()
        driver.find_element_by_css_selector('input[name="username"]').send_keys("tu1@greenletinv.com")
        driver.find_element_by_css_selector('input[name="password"]').clear()
        driver.find_element_by_css_selector('input[name="password"]').send_keys("Test1234")
        driver.find_element_by_css_selector('button[type="submit"]').click()
        time.sleep(5)
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".col-sm-12 h1")))
        self.assertEqual("Entry Homes Dashboard", driver.find_element_by_css_selector(".col-sm-12 h1")
                         .get_attribute("innerText"))
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'a[class="nav-link"][href="/dashboard"]')))
        driver.find_element_by_css_selector('a[class="nav-link"][href="/dashboard"]').click()

    def test_login_with_invalid_credentials_combinations(self):
        """
        Verify user should not be able to login with invalid credential and verify it should give valid error on login
        page
        """
        driver = self.driver
        time.sleep(5)
        wait = WebDriverWait(driver, 60)
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
        driver.find_element_by_css_selector('input[name="username"]').click()
        driver.find_element_by_css_selector('input[name="password"]').click()
        driver.find_element_by_css_selector('button[type="submit"]').click()
        self.assertEqual("Invalid username or password",
                         driver.find_element_by_css_selector('div[role="alert"]').get_attribute("innerText"))
        driver.refresh()
        driver.find_element_by_css_selector('input[name="username"]').clear()
        driver.find_element_by_css_selector('input[name="username"]').send_keys("tu1@greenletinv")
        driver.find_element_by_css_selector('input[name="password"]').clear()
        driver.find_element_by_css_selector('input[name="password"]').send_keys("Test1234")
        driver.find_element_by_css_selector('button[type="submit"]').click()
        self.assertEqual("Invalid username or password",
                         driver.find_element_by_css_selector('div[role="alert"]').get_attribute("innerText"))
        driver.refresh()
        driver.find_element_by_css_selector('input[name="username"]').clear()
        driver.find_element_by_css_selector('input[name="username"]').send_keys("tu1@greenletinv.com")
        driver.find_element_by_css_selector('input[name="password"]').clear()
        driver.find_element_by_css_selector('input[name="password"]').send_keys("test1234")
        driver.find_element_by_css_selector('button[type="submit"]').click()
        self.assertEqual("Invalid username or password",
                         driver.find_element_by_css_selector('div[role="alert"]').get_attribute("innerText"))

    def test_login_page_elements_visibility(self):
        """
        Verify the following elements should be visible on login page
        a. User name input block
        b. Password input block
        c. Entera logo
        d. Submit button
        e. Password reset link
        """
        driver = self.driver
        time.sleep(5)
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, 'input[name="username"]'))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, 'input[name="password"]'))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, 'img[src="/static/media/entera-logo.45256ae9.png"]'))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, 'button[type="submit"]'))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, 'a[href="/reset"]'))

    def test_working_of_password_reset_link(self):
        """
        Verify working of password reset link for valid user id.
        """
        driver = self.driver
        time.sleep(5)
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
        driver.find_element_by_css_selector('a[href="/reset"]').click()

        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'a[href="/signin"]')))

        driver.find_element_by_css_selector('button[type="submit"]').click()

        driver.find_element_by_css_selector('input[name="username"]').clear()
        driver.find_element_by_css_selector('input[name="username"]').send_keys("tu1@greenletinv.com")
        driver.find_element_by_css_selector('button[type="submit"]').click()

        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="alert"]')))
        self.assertEqual("Instructions for how to reset your password have been sent to your email address.",
                         driver.find_element_by_css_selector('div[role="alert"]').get_attribute("innerText"))
        driver.find_element_by_css_selector('a[href="/signin"]').click()

    def test_login_password_reset_with_invalid_user_id(self):
        """
        Verify working of password reset link for invalid user id.
        """
        driver = self.driver
        time.sleep(5)
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
        driver.find_element_by_css_selector('a[href="/reset"]').click()

        driver.find_element_by_css_selector('input[name="username"]').clear()
        driver.find_element_by_css_selector('input[name="username"]').send_keys("abc")
        driver.find_element_by_css_selector('button[type="submit"]').click()
        time.sleep(5)
        self.assertFalse(self.is_element_present(By.CSS_SELECTOR, 'div[role="alert"]'))

    def test_login_reset_password_page_elements_visibility(self):
        """
        Verify the following elements should be visible on reset password page
        a. User id input block
        b. Entera logo
        c. Submit button
        d. Back to login page link
        """
        driver = self.driver
        time.sleep(5)
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
        driver.find_element_by_css_selector('a[href="/reset"]').click()
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,
                                                     'img[src="/static/media/entera-logo.45256ae9.png"]')))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, 'input[name="username"]'))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, 'img[src="/static/media/entera-logo.45256ae9.png"]'))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, 'button[type="submit"]'))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, 'a[href="/signin"]'))

    def test_login_reset_password_message_disappear(self):
        """
        Verify password reset message should disappear when leave password reset page and go back to password reset page
        """
        driver = self.driver
        time.sleep(5)
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
        driver.find_element_by_css_selector('a[href="/reset"]').click()
        driver.find_element_by_css_selector('input[name="username"]').clear()
        driver.find_element_by_css_selector('input[name="username"]').send_keys("tu1@greenletinv.com")
        driver.find_element_by_css_selector('button[type="submit"]').click()
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="alert"]')))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, 'div[role="alert"]'))
        self.assertEqual("Instructions for how to reset your password have been sent to your email address.",
                         driver.find_element_by_css_selector('div[role="alert"]').get_attribute("innerText"))
        driver.find_element_by_css_selector('a[href="/signin"]').click()
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
        driver.find_element_by_css_selector('a[href="/reset"]').click()
        self.assertFalse(self.is_element_present(By.CSS_SELECTOR, 'div[role="alert"]'))

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLoginPage)
    unittest.TextTestRunner(verbosity=2).run(suite)

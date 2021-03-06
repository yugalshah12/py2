# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestLoginWithInvalidCredentialsCombinations(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_login_with_invalid_credentials_combinations(self):
        driver = self.driver
        driver.get("https://frontend.qa.entera.ai/signin")
        driver.find_element_by_css_selector("input[name=\"username\"]").click()
        driver.find_element_by_css_selector("input[name=\"password\"]").click()
        driver.find_element_by_css_selector("button[type=\"submit\"]").click()
        try: self.assertEqual("Invalid username or password", driver.find_element_by_css_selector("div[role=\"alert\"]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.refresh()
        # Warning: verifyTextNotPresent may require manual changes
        try: self.assertNotRegexpMatches(driver.find_element_by_css_selector("BODY").text, "^[\\s\\S]*css=div\\[role=\"alert\"\\][\\s\\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("input[name=\"username\"]").clear()
        driver.find_element_by_css_selector("input[name=\"username\"]").send_keys("tu1@greenletinv")
        driver.find_element_by_css_selector("input[name=\"password\"]").clear()
        driver.find_element_by_css_selector("input[name=\"password\"]").send_keys("Test1234")
        driver.find_element_by_css_selector("button[type=\"submit\"]").click()
        try: self.assertEqual("Invalid username or password", driver.find_element_by_css_selector("div[role=\"alert\"]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.refresh()
        driver.find_element_by_css_selector("input[name=\"username\"]").clear()
        driver.find_element_by_css_selector("input[name=\"username\"]").send_keys("tu1@greenletinv.com")
        driver.find_element_by_css_selector("input[name=\"password\"]").clear()
        driver.find_element_by_css_selector("input[name=\"password\"]").send_keys("test1234")
        driver.find_element_by_css_selector("button[type=\"submit\"]").click()
        try: self.assertEqual("Invalid username or password", driver.find_element_by_css_selector("div[role=\"alert\"]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.close()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

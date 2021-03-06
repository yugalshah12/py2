# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestLoginResetPasswordMessageDisappear(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_login_reset_password_message_disappear(self):
        driver = self.driver
        driver.get("https://frontend.qa.entera.ai/signin")
        for i in range(60):
            try:
                if driver.find_element_by_css_selector("input[name=\"username\"]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_css_selector("a[href=\"/reset\"]").click()
        driver.find_element_by_css_selector("input[name=\"username\"]").clear()
        driver.find_element_by_css_selector("input[name=\"username\"]").send_keys("tu1@greenletinv.com")
        driver.find_element_by_css_selector("button[type=\"submit\"]").click()
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div[role=\"alert\"]"))
        try: self.assertEqual("Instructions for how to reset your password have been sent to your email address.", driver.find_element_by_css_selector("div[role=\"alert\"]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("a[href=\"/signin\"]").click()
        for i in range(60):
            try:
                if driver.find_element_by_css_selector("input[name=\"username\"]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_css_selector("a[href=\"/reset\"]").click()
        self.assertFalse(self.is_element_present(By.CSS_SELECTOR, "div[role=\"alert\"]"))
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

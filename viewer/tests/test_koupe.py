# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TestTestkoupe():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_testkoupe(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.set_window_size(1200, 910)
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(3)
        self.driver.find_element(By.ID, "id_username").send_keys("1234")  # Přihlašovací údaje
        self.driver.find_element(By.ID, "id_password").send_keys("1234")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "form > p:nth-child(2)").click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(3)").click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        time.sleep(3)
        self.driver.find_element(By.LINK_TEXT, "Paintings").click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR,
                                 ".u-align-center:nth-child(1) .u-align-center:nth-child(6) > .btn").click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, "form:nth-child(15) > button").click()
        time.sleep(3)
        self.driver.find_element(By.LINK_TEXT, "Proceed to payment").click()
        time.sleep(3)

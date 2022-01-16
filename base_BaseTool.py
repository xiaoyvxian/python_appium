#!/usr/bin/env python3

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, driver):
        # self.driver = AndroidDriver.driver
        self.driver = driver

    def locator(self, loc):
        return self.driver.find_element(*loc)

    def click(self, loc):
        self.locator(loc).click()

    def elementWait(self, times, loc):
        try:
            wait = WebDriverWait(self.driver, times, 0.2)
            wait.until(EC.presence_of_element_located(loc))
            return True
        except:
            return False

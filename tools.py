from AndroidDriver import AndroidDriver


class BasePage:

    def __init__(self):
        self.driver = AndroidDriver.driver

    def locator(self, loc):
        return self.driver.find_element(*loc)

    def click(self, loc):
        self.locator(loc).click()

from appium import webdriver

desired_caps = {'platformName': 'Android',
                }


class AndroidDriver:
    driver = webdriver

    @classmethod
    def startup(cls, device_dict, apppackage=None, appactivity=None):
        # 'com.ontim.camera2', 'com.ontim.camera2.CameraLauncher'
        desired_caps['appPackage'] = apppackage
        desired_caps['appActivity'] = appactivity
        desired_caps['udid'] = device_dict['udid']
        desired_caps['systemPort'] = device_dict['system_port']
        desired_caps['platform_version'] = device_dict['platform_version']
        server_port = device_dict['server_port']
        cls.driver = webdriver.Remote(f'http://127.0.0.1:{server_port}/wd/hub', desired_caps)
        return cls.driver

    def locator(self, loc):
        return self.driver.find_element(*loc)

    def click(self, loc):
        self.locator(loc).click()

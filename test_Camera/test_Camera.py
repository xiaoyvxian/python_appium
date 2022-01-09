import configparser
import time
from selenium.webdriver.common.by import By
from androidDriver import AndroidDriver
from tools import BasePage

device_dict = dict


def readinfo():
    conf = configparser.ConfigParser()
    conf.read('info.ini')
    global device_dict
    device_dict = {}
    for location in conf.options('device_dict'):
        key = location
        value = conf.get('device_dict', location)
        device_dict[key] = value


shutter_button = (By.ID, "com.ontim.camera2:id/mode_shutter_button")


class TestCam(AndroidDriver):

    # 函数级的（setup_function、teardown_function）只对函数用例生效，而且不在类中使用
    # 类级的（setup_class、teardown_class）在类中使用，类执行之前运行一次，类执行之后运行一次
    # 类中方法级的（setup_method、teardown_method）在每一个方法之前执行一次，在每一个方法之后执行一次
    # 模块级的（setup_module、teardown_module）全局的，在模块执行前运行一遍，在模块执行后运行一遍
    def setup_class(self):
        readinfo()
        self.driver = AndroidDriver.startup(device_dict)
        print(self.driver)
        self.driver.implicitly_wait(10)
        self.driver.start_activity('com.ontim.camera2', 'com.ontim.camera2.CameraLauncher')
        # self.phones[1].start_activity('com.ontim.camera2', 'com.ontim.camera2.CameraLauncher')

    def setup_method(self):
        print("222")
        # AndroidDriver.startup('com.ontim.camera2', 'com.ontim.camera2.CameraLauncher')
        time.sleep(2)
        self.driver.start_activity('com.ontim.camera2', 'com.ontim.camera2.CameraLauncher')
        # self.phones[1].start_activity('com.ontim.camera2', 'com.ontim.camera2.CameraLauncher')
        # AndroidDriver.startup('com.ontim.camera2', 'com.ontim.camera2.CameraLauncher')

    def teardown_method(self):
        print("555")
        for _ in range(3):
            self.driver.keyevent(4)
            # self.phones[1].keyevent(4)
        self.driver.keyevent(3)
        # self.phones[1].keyevent(3)

    def test_01(self):
        print("333")
        # self.phones[0].find_element(By.ID, "com.ontim.camera2:id/mode_shutter_button").click()
        # self.phones[1].find_element(By.ID, "com.ontim.camera2:id/mode_shutter_button").click()
        BasePage().click(shutter_button)

        time.sleep(2)

    def test_02(self):
        print("444")
        time.sleep(2)
        self.driver.find_element(By.ID, "com.ontim.camera2:id/mode_shutter_button").click()
        # self.phones[1].find_element(By.ID, "com.ontim.camera2:id/mode_shutter_button").click()
        self.driver.find_element_by_accessibility_id()
        time.sleep(2)


if __name__ == '__main__':
    a = TestCam()
    a.setup_class()
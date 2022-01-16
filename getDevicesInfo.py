import configparser
import os
import socket
from pathlib import Path

import serial.tools.list_ports
from appium import webdriver


def cmd(command) -> str:
    result = os.popen(command).read()
    return result


def get_devices_sn() -> list:
    devices = cmd('adb devices').replace("List of devices attached", "").replace("\n", "").replace(
        "device",
        "").split(
        "\t")
    devices.pop(-1)
    if "unauthorized" in devices or len(devices) == 0:
        raise Exception('获取SN号失败：设备未授权')
    return devices


def check_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.shutdown(2)
    except OSError:
        return True
    else:
        return False


class TestPhone:
    def __init__(self, device, i):
        self.driver = webdriver
        self.device = device
        self.version = self.get_devices_version()
        # self.android_version = self.get_devices_android_version(self.device)
        self.info = self.get_device_infos(i)
        self.port = self.get_devices_port()

    def get_devices_version(self):
        version = cmd(f"adb -s {self.device} shell getprop ro.versions.internal_sw_ver").replace("\n", "") + "_" + cmd(
            f"adb -s {self.device} shell getprop ro.elabel.ontim.version").replace("\n", "")
        return version

    @classmethod
    def get_devices_android_version(cls, device) -> str:
        if not isinstance(device, str):
            raise Exception("device type is should str..")
        result = cmd("adb -s {} shell getprop ro.build.version.release".format(device)).strip()
        result = result.strip()
        if "error" not in result:
            return result
        else:
            raise Exception("获取设备安卓系统版本失败")

    def get_device_infos(self, i) -> dict:
        device_dict = {"platform_version": TestPhone.get_devices_android_version(self.device),
                       "server_port": 4723 + i * 2,
                       "system_port": 8200 + i * 1,
                       "udid": self.device,
                       "port": self.get_devices_port()}
        if check_port(host='127.0.0.1', port=device_dict["server_port"]):
            return device_dict
        else:
            raise Exception(device_dict["server_port"].__str__() + "端口被占用，启动失败")

    def get_devices_port(self):
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            if 'LTE' in port.description:
                # print(port.name)
                if port.serial_number == self.device:
                    return port.name
                # todo:补全在没有驱动的情况下的报错信息

    def white_info(self):
        conf = configparser.ConfigParser()
        conf.read('info.ini')
        conf.add_section('PhoneInfo')
        conf.set('PhoneInfo', 'version', self.version)
        conf.add_section('device_dict')
        for _ in self.info:
            conf.set('device_dict', _, str(self.info[_]))
        with open(Path(f"{os.getcwd()}/accomplish/{self.device}/info.ini"), 'w') as file:
            conf.write(file)
            file.close()


if __name__ == '__main__':
    phones = []
    for i, sn in enumerate(get_devices_sn()):
        phone = TestPhone(device=sn, i=i)
        phones.append(phone)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import sys
import time

import pytest
from selenium.webdriver.common.by import By

sys.path.append('../..')

import AndroidDriver
from base_BaseTool import BasePage
from tool_sendAT import sendAT
from base_OtherTool import OtherTool

calltime = 3

conf = configparser.ConfigParser()
conf.read('info.ini')
dev = conf.get('device_dict', 'udid')
port = conf.get('device_dict', 'port')

on_bsn = "AT+CFUN=1;"
off_bsn = "AT+CFUN=2;"
SIM1 = "AT+SPACTCARD=0"
SIM2 = "AT+SPACTCARD=1"
cm_bsn = "ATD10086;"
cu_bsn = "ATD10010;"
on_sfun = "AT+SFUN=5;"
off_sfun = "AT+SFUN=4;"
H_G = "AT+SPTESTMODEM=10, 14"
LTE = "AT+SPTESTMODEM=6, 6"

end_call = (By.ID, "com.google.android.dialer:id/incall_end_call")
talk_time = (By.ID, "com.google.android.dialer:id/contactgrid_bottom_timer")

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


class Test_Modem(OtherTool):

    def setup_class(self):
        readinfo()
        appPackage = "com.google.android.dialer"
        appActivity = "com.google.android.dialer.extensions.GoogleDialtactsActivity"
        # AndroidDriver.AndroidDriver().startup(appactivity=appPackage, apppackage=appActivity, device_dict=device_dict)
        self.driver = AndroidDriver.AndroidDriver.startup(device_dict)
        self.driver.implicitly_wait(10)
        self.driver.start_activity(appPackage, appActivity)
        time.sleep(10)

    @pytest.mark.repeat(500)
    def test_callTo_SIM1(self):
        try:
            assert self.StationedStatus(dev)[0] == "IN_SERVICE", '手机脱网!!'
            assert self.StationedStatus(dev)[1] == "IN_SERVICE", '手机脱网!!'
            sendAT(port=port, bsn=SIM1)
            time.sleep(2)
            sendAT(port=port, bsn=cm_bsn)
            try:
                if BasePage().elementWait(20, talk_time):
                    for i in range(calltime):
                        time.sleep(1)
                        assert self.StationedStatus(dev)[0] == "IN_SERVICE", '手机脱网!!'
                        assert self.networkmode(dev)[0] == "LTE", "非4G网络!!"
                        assert self.StationedStatus(dev)[1] == "IN_SERVICE", '手机脱网!!'
                        assert self.networkmode(dev)[1] == "LTE", "非4G网络!!"
                    BasePage().click(end_call)
                    time.sleep(5)
            except:
                BasePage().click(end_call)
        except:
            BasePage().click(end_call)

    @pytest.mark.repeat(500)
    def test_callTo_SIM2(self):
        try:
            assert self.StationedStatus(dev)[1] == "IN_SERVICE", '手机脱网!!'
            assert self.StationedStatus(dev)[0] == "IN_SERVICE", '手机脱网!!'
            sendAT(port=port, bsn=SIM2)
            time.sleep(2)
            sendAT(port=port, bsn=cu_bsn)
            try:
                if BasePage().elementWait(20, talk_time):
                    for i in range(calltime):
                        time.sleep(1)
                        assert self.StationedStatus(dev)[1] == "IN_SERVICE", '手机脱网!!'
                        assert self.networkmode(dev)[1] == "LTE", "非4G网络!!"
                        assert self.StationedStatus(dev)[0] == "IN_SERVICE", '手机脱网!!'
                        assert self.networkmode(dev)[0] == "LTE", "非4G网络!!"
                    BasePage().click(end_call)
                    time.sleep(5)
            except:
                BasePage().click(end_call)
        except:
            BasePage().click(end_call)

    @pytest.mark.repeat(500)
    def test_power_SIM1(self):
        sendAT(port=port, bsn=SIM1)
        time.sleep(2)
        sendAT(port=port, bsn=off_bsn)
        time.sleep(2)
        sendAT(port=port, bsn=on_bsn)
        time.sleep(60)
        assert self.StationedStatus(dev)[0] == "IN_SERVICE", '手机脱网!!'
        assert self.networkmode(dev)[0] == "LTE", "非4G网络!!"
        assert self.StationedStatus(dev)[1] == "IN_SERVICE", '手机脱网!!'
        assert self.networkmode(dev)[1] == "LTE", "非4G网络!!"

    @pytest.mark.repeat(500)
    def test_power_SIM2(self):
        sendAT(port=port, bsn=SIM2)
        time.sleep(2)
        sendAT(port=port, bsn=off_bsn)
        time.sleep(2)
        sendAT(port=port, bsn=on_bsn)
        time.sleep(60)
        assert self.StationedStatus(dev)[1] == "IN_SERVICE", '手机脱网!!'
        assert self.networkmode(dev)[1] == "LTE", "非4G网络!!"
        assert self.StationedStatus(dev)[0] == "IN_SERVICE", '手机脱网!!'
        assert self.networkmode(dev)[0] == "LTE", "非4G网络!!"

    @pytest.mark.repeat(500)
    def test_Networkswitch(self):
        on_airplanemode()
        Networkswitch2G3G()
        off_airplanemode()
        try:
            assert self.networkmode(dev)[0] == "EDGE"
            assert self.StationedStatus(dev)[0] == "IN_SERVICE", '手机脱网!!'
            assert self.networkmode(dev)[1] == "UMTS"
            assert self.StationedStatus(dev)[1] == "IN_SERVICE", '手机脱网!!'
            on_airplanemode()
            Networkswitch4G()
            off_airplanemode()
            assert self.networkmode(dev)[0] == "LTE"
            assert self.StationedStatus(dev)[0] == "IN_SERVICE", '手机脱网!!'
            assert self.networkmode(dev)[1] == "LTE"
            assert self.StationedStatus(dev)[0] == "IN_SERVICE", '手机脱网!!'
        except:
            on_airplanemode()
            Networkswitch4G()
            off_airplanemode()
            assert self.networkmode(dev)[0] == "LTE"
            assert self.StationedStatus(dev)[0] == "IN_SERVICE", '手机脱网!!'
            assert self.networkmode(dev)[1] == "LTE"
            assert self.StationedStatus(dev)[0] == "IN_SERVICE", '手机脱网!!'


def on_airplanemode():
    sendAT(port=port, bsn=SIM1)
    time.sleep(2)
    sendAT(port=port, bsn=on_sfun)
    time.sleep(2)
    sendAT(port=port, bsn=SIM2)
    time.sleep(2)
    sendAT(port=port, bsn=on_sfun)
    time.sleep(2)


def off_airplanemode():
    sendAT(port=port, bsn=SIM1)
    time.sleep(2)
    sendAT(port=port, bsn=off_sfun)
    time.sleep(2)
    sendAT(port=port, bsn=SIM2)
    time.sleep(2)
    sendAT(port=port, bsn=off_sfun)
    time.sleep(60)


def Networkswitch2G3G():
    sendAT(port=port, bsn=H_G)
    time.sleep(2)


def Networkswitch4G():
    sendAT(port=port, bsn=LTE)
    time.sleep(2)

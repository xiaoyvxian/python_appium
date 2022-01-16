#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

import getDevicesInfo


class OtherTool:

    def callStatus(self, dev):
        cmdstatus = os.popen("adb -s " + dev + " shell dumpsys telephony.registry|grep -E ^mCallState")
        status = cmdstatus.buffer.read().decode('utf-8')
        var_SIM1 = re.split(r'    ', str(status))[1]
        var_SIM1 = re.split(r'=', str(var_SIM1))[1]
        var_SIM2 = re.split(r'    ', str(status))[2]
        var_SIM2 = re.split(r'=', str(var_SIM2))[1]
        return var_SIM1[:1], var_SIM2[:1]

    def networkStatus(self):
        try:
            cmdstatus = os.popen('adb shell dumpsys netstats|grep -A 1 "^Active interfaces:"')
            status = cmdstatus.buffer.read().decode('utf-8')
            var = re.split(r'\[\{', str(status))[1]
            var = re.split(r'=', str(var))[1]
            var = re.split(r',', str(var))[0]
            return var
        except:
            return False

    def StationedStatus(self, dev):
        cmdstatus = os.popen(
            'adb  -s ' + dev + ' shell dumpsys telephony.registry|grep -A 1 ^getRilVoiceRadioTechnology')
        status = cmdstatus.buffer.read().decode('utf-8')
        var_SIM1 = re.split(r'--', str(status))[0]
        var_SIM1 = re.split(r',', str(var_SIM1))[0]
        var_SIM1 = re.split(r'\(', str(var_SIM1))[1]
        var_SIM1 = re.split(r'\)', str(var_SIM1))[0]
        var_SIM2 = re.split(r'--', str(status))[1]
        var_SIM2 = re.split(r',', str(var_SIM2))[0]
        var_SIM2 = re.split(r'\(', str(var_SIM2))[1]
        var_SIM2 = re.split(r'\)', str(var_SIM2))[0]
        return var_SIM1, var_SIM2

    def networkmode(self, dev):
        cmdstatus = os.popen(
            "adb -s " + dev + " shell dumpsys telephony.registry|grep -A 1 ^getRilVoiceRadioTechnology")
        status = cmdstatus.buffer.read().decode('utf-8')
        var_SIM1 = re.split(r'--', str(status))[0]
        var_SIM1 = re.split(r',', str(var_SIM1))[8]
        var_SIM1 = re.split(r'\(', str(var_SIM1))[1]
        var_SIM1 = re.split(r'\)', str(var_SIM1))[0]
        var_SIM2 = re.split(r'--', str(status))[1]
        var_SIM2 = re.split(r',', str(var_SIM2))[8]
        var_SIM2 = re.split(r'\(', str(var_SIM2))[1]
        var_SIM2 = re.split(r'\)', str(var_SIM2))[0]
        return var_SIM1, var_SIM2


if __name__ == '__main__':
    for i in getDevicesInfo.get_devices_sn():
        print(OtherTool().callStatus(i))
        print(OtherTool().StationedStatus(i))
        print(OtherTool().networkmode(i))

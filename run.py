import configparser
import os
import shutil
import sys
import time
from pathlib import Path

import getDevicesInfo


def log_dir(sn):
    return Path(os.getcwd() + f"/accomplish/{sn}")


def ready_to_test():
    system_type = sys.platform
    a = os.popen('REG QUERY HKEY_CURRENT_USER\Console /v QuickEdit').read()
    if '0x1' in a:
        os.popen('reg add HKEY_CURRENT_USER\Console /v QuickEdit /t REG_DWORD /d 00000000 /f')
        print('已尝试将CMD‘快速编辑模式’设为关闭状态')

    for i, sn in enumerate(getDevicesInfo.get_devices_sn()):
        source_path = Path(os.getcwd() + "/test_Camera")
        target_path = Path(os.getcwd() + "/accomplish/" + sn)
        if os.path.exists(target_path):
            conf = configparser.ConfigParser()
            conf.read(Path(os.getcwd() + "/accomplish/" + sn + "/info.ini"))
            post = int(conf.get('device_dict', 'server_port'))
            if getDevicesInfo.check_port(host='127.0.0.1', port=post):
                pass
            else:
                raise Exception(post.__str__() + "端口被占用，启动失败")
            if 'win' in system_type:
                shell(system_type='win',
                      comlist=[[f'appium -p {post} --log {log_dir(sn=sn)}\Appium_log.log']])

            elif 'linux' in system_type:
                shell(system_type='linux',
                      comlist=[[f'appium -p {post} --log {log_dir(sn=sn)}/Appium_log.log']])
            else:
                raise Exception("获取PC操作系统失败")

        else:
            phone = getDevicesInfo.TestPhone(device=sn, i=i)
            shutil.copytree(source_path, target_path)
            phone.white_info()
            post = phone.info['server_port']
            if 'win' in system_type:
                shell(system_type='win',
                      comlist=[[f'appium -p {post} --log {log_dir(sn=phone.device)}\Appium_log.log']])

            elif 'linux' in system_type:
                shell(system_type='linux',
                      comlist=[[f'appium -p {post} --log {log_dir(sn=phone.device)}/Appium_log.log']])
            else:
                raise Exception("获取PC操作系统失败")


def shell(system_type, comlist):
    """
    :param system_type: 执行脚本的操作系统类型
    :param comlist: 为命令组成的二维列表，每个子列表代表从单个标签页中依次运行的命令
    """
    if system_type == 'win':
        for labelCom in comlist:
            command = 'start cmd /k'
            command += ' "'
            for com in labelCom:
                command += f' {com}&'
            command += '"'
            print(command)
            os.popen(command)
    elif system_type == 'linux':
        command = "gnome-terminal"
        print(len(comlist))
        for labelCom in comlist:
            if labelCom == comlist[0]:
                command += " --window -e 'bash -c \""
                for com in labelCom:
                    command = command + com + "; "
                command += "exec bash\"' "
            else:
                command += "--tab -e 'bash -c \""
                for com in labelCom:
                    command = command + com + "; "
                command += "exec bash\"' "
        os.system(command)


if __name__ == '__main__':
    ready_to_test()
    time.sleep(2)
    system_type = sys.platform
    if 'win' in system_type:
        for sn in getDevicesInfo.get_devices_sn():
            comlist = [
                [f"cd accomplish\{sn}",
                 "python -m pytest test_Camera.py -vs --instafail --tb=long --capture=sys --html=pytest_log.html"],
                # [f"set ANDROID_SERIAL={sn}", f"cd accomplish\{sn}\getLogs\Dropbox", "python getDropbox_v0.6.py"],
                # [f"set ANDROID_SERIAL={sn}", "adb shell ps -A |findstr system_server"]
            ]
            shell(system_type='win', comlist=comlist)
    elif 'linux' in system_type:
        for sn in getDevicesInfo.get_devices_sn():
            comlist = [
                [f"cd accomplish/{sn}",
                 "python -m pytest -vs --instafail --tb=long --capture=sys --html=pytest_log.html"],
                [f"export ANDROID_SERIAL={sn}", f"cd accomplish/{sn}/getLogs/Dropbox", "python3 getDropbox_v0.6.py"],
                [f"export ANDROID_SERIAL={sn}", "adb shell ps -A |grep system_server"]
            ]
            shell(system_type='linux', comlist=comlist)
    else:
        raise Exception("获取PC操作系统失败")

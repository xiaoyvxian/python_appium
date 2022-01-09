import os
import time

DIR = os.getcwd() + os.sep
print(os.system('adb shell getprop ro.versions.internal_sw_ver'))


def pullOutLogs():
    """
    Pull out the BP Log to PC
    """
    for i in range(1000):
        local_time = time.strftime('%Y-%m-%d-%H.%M.%S', time.localtime(time.time()))
        dropbox = os.path.join(DIR, "dropbox")
        current_dropbox = os.path.join(dropbox, local_time)
        if not os.path.exists(current_dropbox):
            os.makedirs(current_dropbox)
        loginfo = os.path.join(current_dropbox, "log_info.txt")
        os.system('adb shell dumpsys dropbox --print > %s' % loginfo)
        time.sleep(21600)


if __name__ == '__main__':
    pullOutLogs()
    input('press Enter key to exit...')

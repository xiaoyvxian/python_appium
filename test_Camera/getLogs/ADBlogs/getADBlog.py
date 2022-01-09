#!/usr/bin/env python
import os
import shutil
import subprocess
import string
import time
import io


DIR = os.getcwd() + os.sep
#eventLog_Name = '0430_u4_events.log'
#os.environ['PATH'] += ':/home/xiaobowen/android-sdk-linux/platform-tools'

def pullOutLogs():
    '''
    Pull out the BP Log to PC
    '''

    os.system('adb root')
    os.system('adb remount')
    print(DIR)
    for i in range(1000):
        level = []
        system_server = []
        print(("*"*50))
        #os.system('adb shell dumpsys battery | grep "level"')
        #os.system('adb shell ps -A |grep system_server')
        print(("*"*50))
        # Set the PC local time as the result folder name.
        local_time = time.strftime('%Y-%m-%d-%H.%M.%S', time.localtime(time.time()))

        if os.path.exists(DIR + "level.log") == False:  #
            io.open(str(DIR + "level.log"), 'w', encoding="utf-8")
        os.system('adb shell dumpsys battery | grep level > level.txt')
        with io.open(str(DIR + "level.txt"), "r") as file:
            level_ = file.read()
        with io.open(str(DIR + "level.log"), "a") as file:
            file.write('' + local_time + " " + level_ + "\n")
        os.system('rm -f ' + DIR + "level.txt")

        if os.path.exists(DIR + "system_server.log") == False:  #
            io.open(str(DIR + "system_server.log"), 'w', encoding="utf-8")
        os.system('adb shell ps -A |grep system_server > system_server.txt')
        with io.open(str(DIR + "system_server.txt"), "r") as file:
            system_server = file.read()
        with io.open(str(DIR + "system_server.log"), "a") as file:
            file.write('' + local_time + " " + system_server + "\n")
        os.system('rm -f ' + DIR + "system_server.txt")

        # Pull out result
        os.system('mkdir %s%s'%(DIR,local_time))
        subprocess.Popen("adb  logcat -v time > ."+os.sep+local_time+os.sep+"aplog.log", shell=True)
        subprocess.Popen("adb  logcat -v time -b radio> ."+os.sep+local_time+os.sep+"radio.log" , shell=True)
        subprocess.Popen("adb  logcat -v time -b main> ." + os.sep + local_time + os.sep + "system.log", shell=True)
        subprocess.Popen("adb  logcat -v time -b events> ." + os.sep + local_time + os.sep + "events.log", shell=True)
        subprocess.Popen("adb shell  cat /proc/kmsg  > ." + os.sep + local_time + os.sep + "kmsg.log", shell=True)
        subprocess.Popen("adb shell dmesg -w > ." + os.sep + local_time + os.sep + "dmsg.log", shell=True)
        subprocess.Popen("adb pull /data/local/tmp/hprof.hprof > ." + os.sep + local_time + os.sep + "dmsg.log", shell=True)


        time.sleep(1800)

        pidinfo=os.popen("adb shell ps | grep logcat")
        for line in pidinfo:
            # print line
            pid=line.split(" ")[6]
            # print pid
            #print pid
            os.system("adb shell kill %s "%pid)

        os.system("adb pull /data/anr ." + os.sep + local_time + os.sep)
        time.sleep(3)
        os.system('zip -r %s.zip ./%s'%(local_time,local_time))
        # Delete result folder
        
        shutil.rmtree('%s%s'%(DIR,local_time))
        # Pull out offline log per 1 hour.


if __name__=='__main__':
    pullOutLogs()

input('press Enter key to exit...')

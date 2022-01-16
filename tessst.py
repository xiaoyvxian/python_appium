import os
import sys

system_type = sys.platform
a = os.popen('REG QUERY HKEY_CURRENT_USER\Console /v QuickEdit').read()
if '0x0' in a:
    print('关闭')
elif '0x1' in a:
    print('未关闭')
    os.popen('reg add HKEY_CURRENT_USER\Console /v QuickEdit /t REG_DWORD /d 00000000 /f')

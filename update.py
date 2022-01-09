import hashlib
import os
import zipfile
from ftplib import FTP
import ftplib


class UpDate:
    def __init__(self):
        self.dir = os.getcwd()
        self.make_zip(self.dir)
        self.zipname = f'{os.path.basename(self.dir)}.zip'
        self.md5 = self.get_file_md5(f'UPdate{os.sep}{self.zipname}')
        self.ftp = FTP()
        self.up_to_FTP()

    def make_zip(self, dir):
        """
        用于创建LOG压缩包
        """
        zipname = os.path.basename(self.dir)
        if os.path.exists('UPdate'):
            pass
        else:
            os.makedirs('UPdate')
        z = zipfile.ZipFile('UPdate' + os.sep + zipname + ".zip", 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(dir):
            fpath = dirpath.replace(dir, '')
            fpath = fpath and fpath + os.sep or ''
            if 'UPdate' in fpath:
                continue
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()

    def get_file_md5(self, filename):  # 产生MD5值
        if not os.path.isfile(filename):
            raise Exception('脚本压缩包路径存在问题')
        myhash = hashlib.md5()
        f = open(filename, 'rb')
        while True:
            b = f.read(1024)
            if not b:
                break
            myhash.update(b)
        f.close()
        txt = open('UPdate' + os.sep + 'MD5', 'w')
        txt.write(myhash.hexdigest())
        txt.close()
        return myhash.hexdigest()

    def trytopath(self, path):
        """
        尝试进入目录
        如果目录不存在则创建一个
        """
        try:
            self.ftp.cwd(path)
        except ftplib.error_perm:
            self.ftp.mkd(path)
            self.ftp.cwd(path)

    def up_to_FTP(self):
        self.ftp.connect("192.168.0.224")
        self.ftp.login("ontimneibu", "HGJ3yL")
        print(self.ftp.getwelcome())
        # print(self.ftp.dir())
        self.trytopath('Log')
        self.trytopath('script')
        self.trytopath('Camera')
        bufsize = 1024
        with open(f'UPdate{os.sep}{self.zipname}', 'rb') as f:
            self.ftp.storbinary("STOR %s" % self.zipname, f, bufsize)
        with open(f'UPdate{os.sep}MD5', 'rb') as f:
            self.ftp.storbinary("STOR %s" % 'MD5', f, bufsize)


a = UpDate()

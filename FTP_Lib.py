import ftplib
from ftplib import FTP
import os
import time
from datetime import datetime


class MyFTP:
    def __init__(self, ip, user, pw):
        self.ip = ip
        self.user = user
        self.pw = pw
        self.ftp = None

    def login(self):
        self.ftp = FTP(self.ip)
        self.ftp.login(user=self.user, passwd=self.pw)
        current_directory = self.ftp.pwd()
        print("Login-OK")
        print("Current directory:", current_directory)

    def upload_file(self, remote_folder, local_path, remote_filename):
        remote_path = remote_folder + '/' + remote_filename
        with open(local_path, 'rb') as file:
            self.ftp.storbinary('STOR ' + remote_path, file)
        print("Upload completed.")

    def download_file(self, remote_folder, remote_filename, local_path):
        remote_path = remote_folder + '/' + remote_filename

        # 檢查本地資料夾是否存在，如果不存在則建立
        if not os.path.exists('local_folder'):
            os.makedirs('local_folder')

        # 檢查 'local_folder/bak' 資料夾是否存在，如果不存在則建立
        if not os.path.exists('local_folder/bak'):
            os.makedirs('local_folder/bak')

        # 下載圖片檔案
        with open(local_path, 'wb') as file:
            self.ftp.retrbinary('RETR ' + remote_path, file.write)
        # print("Image download completed.")

    def logout(self):
        self.ftp.quit()
        print("Logout.")

    def ftpdir(self):
        directory_contents = []
        self.ftp.dir(directory_contents.append)
        print("Directory contents:")
        for item in directory_contents:
            print(item)

    def count_files_in_directory(self, remote_directory):
        filist = []
        self.ftp.cwd(remote_directory)  # 切換到指定的遠端目錄
        file_list = self.ftp.nlst()  # 取得目錄內的檔案清單
        file_count = len(file_list)  # 計算檔案數量
        print(f"Number of files in directory '{remote_directory}': {file_count}")

        for file_name in file_list:
            filist.append(file_name)

        return filist

    def go_to_parent_directory(self):
        self.ftp.cwd("..")  # 切換到上一層目錄
        current_directory = self.ftp.pwd()
        print("Current directory:", current_directory)

    def move_file(self, source_folder, target_folder, filename):
        source_path = source_folder + '/' + filename
        target_path = target_folder + '/ok_' + filename

        try:
            self.ftp.rename(source_path, target_path)
            # print("File moved successfully.")
        except ftplib.error_perm as e:
            print("Error moving file:", str(e))


# 建立 FTP 物件並執行登入


# my_ftp = MyFTP('66.220.9.50', 'b79922331', 'becky800611')
my_ftp = MyFTP('209.97.161.199', 'ftpuser1', 'ji3m/4ftp')
remoteDir = 'ipcam01'
bk_folder = 'bk'
#
my_ftp.login()
my_ftp.ftpdir()
# current_time = datetime.now()
# formatted_time = current_time.strftime("%Y%m%d%H%M%S")
#
# # 上傳檔案
# # my_ftp.upload_file(remoteDir, 'dog.jpg', 'ddog.jpg')
# # print(my_ftp.count_files_in_directory(remoteDir))
#
# # 單筆下載檔案
# my_ftp.download_file(remoteDir, '192.168.10.171_01_20230522160447836_TIMING.jpg', "local_folder\\"+"下載來的.jpg")
# try :


# remotefile= '192.168.10.171_01_20230611173131359_TIMING.jpg'

filist = my_ftp.count_files_in_directory(remoteDir)

my_ftp.go_to_parent_directory()
my_ftp.ftpdir()
total_num = len(filist)
cont_num = 1
for i in filist:
    # my_ftp.ftpdir()

    print("總共有%d檔案,正在處理第%d檔案,目前尚餘%d個檔案" % (total_num, cont_num, total_num - cont_num))

    str_list = i.split('_')
    name = str_list[2]

    my_ftp.download_file(remoteDir, i, 'local_folder\\' + name[:12]+".jpg")
    # print(i, ' 已上傳')

    my_ftp.move_file(remoteDir, bk_folder , i)
    cont_num=cont_num+1
# 登出

try:
    my_ftp.logout()
    print("Logout successful.")
except Exception as e:
    print("Logout failed:", str(e))
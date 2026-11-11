from socket import *   # socket网络通信模块
import pickle
S = socket()           # 等待连接的socket
S.bind((gethostname(), 8080))
S.listen()
s, addr = S.accept()

# 接受服务器的数据
while True:
    st = s.recv(1024).decode()
    if st == '0':
        break
    s.send('1'.encode())
    data_list = pickle.loads(s.recv(1024))
    print(data_list)
    s.send('1'.encode())
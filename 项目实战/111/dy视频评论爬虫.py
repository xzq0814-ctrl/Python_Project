# [网页自动化]-[爬虫] requests爬不下来的数据
# 自动化=纯模拟手工
import matplotlib.pyplot
from wordcloud import WordCloud  # 词云  舆论分析 检测的常用手段
from DrissionPage import *
import re
text_str = '' # 准备一个空字符串
# 1.打开浏览器
page = ChromiumPage()  # 打开一个浏览器对象 取名page
page.listen.start('comment/list') #告诉浏览器，待会访问网址时把含有这个关键词挑出来
# 2.输入视频网址(博主主页视频) 按回车
url = 'https://www.douyin.com/user/MS4wLjABAAAAx-mH1oMVAHDSCU4YM-_AnJyAK7wYYxYQeGniL_dmZw4BBbkZ-rLoRxon6WTbjrRd?from_tab_name=main&modal_id=7388891708383137078'
page.get(url)  #访问这个网址 ,但没找到评论
# 3.定位评论按钮元素  拿到评论数据
page.wait(2)
ele1 = page.ele('css:.jp8u3iov')  # 定位评论按钮
ele1.click()                      #点击评论按钮
for i in range(50):
    result = page.listen.wait() # 阻塞程序，直到出现监听的目标链接为止
    # 监听到的数据中提取链接url 导入requests  response = requests.get(url) json_data = response.json()
    json_data = result.response.body
    comments = json_data['comments']
    for comment in comments:
        text = comment['text']
        text_str += text + '\n'    # 评论汇总
        nickname = comment['user']['nickname']
        ip = comment['ip_label']
        homepage = 'https://www.douyin.com/user/' + comment['user']['sec_uid']
        print(f'来自【{ip}】的【{nickname}】说：{text}  主页：{homepage}')
    # 4.想看更多 鼠标滑轮滚动评论区(出现加载) 加载后获取更多评论
    try:
        ele2 = page.ele('加载中')
        page.scroll.to_see(ele2)  # 浏览器.滚.直到看见ele2
    except:
        break
# 循环结束之后
open('视频评论数据.txt','w',encoding='utf-8').write(text_str)
text = open('视频评论数据.txt','r',encoding='utf-8').read()
text = re.sub(r'\[.*?]','', text)
wc = WordCloud(font_path='C:/Windows/Fonts/msyh.ttc', width=1920, height=1080, background_color='white').generate(text)
matplotlib.pyplot.imshow(wc)
matplotlib.pyplot.show()

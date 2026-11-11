"""
提取主页面中每一个电影背后的url地址
    拿到"2025必看热片"那一块的HTML代码
    从代码中提取href的值  (href为网页文字对应的背后的链接)
访问子页面，提取到页面的名称以及下载地址
    拿到子页面的页面源代码
    提取数据
"""
import requests
import re
f = open("2025热片.csv",mode="w",encoding="utf-8")
url = "https://www.dytt8899.com/"
resp = requests.get(url)
resp.encoding = "gbk"
# print(resp.text)
# 从电影天堂主页面筛选出2025必看热片的正则表达
obj1 = re.compile(r'2025必看热片.*?<ul>(?P<html>.*?)</ul>', re.S)
result1 = obj1.search(resp.text)  # 页面只有一个此内容可以用search
# print(result1.group("html"))
# 从2025必看热片中提取每个电影的href网址
obj2 = re.compile(r"<li><a href='(?P<href>.*?)' title=")
result2 = obj2.finditer(result1.group("html")) # 页面很多相似的正则表达  iter 要用for循环
# id 一般是整个网页里唯一的值，可以用id定位
# 将每个href网址对应的电影信息以及下载链接提取出来
obj3 = re.compile(r'片　　名　(?P<movie>.*?)<br />.*?产　　地　(?P<location>.*?)<br />.*?'
                  r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<link>.*?)">', re.S)
for item in result2:
    child_url = f"https://www.dytt8899.com{item.group("href")}"
    resp2 = requests.get(child_url)
    resp2.encoding = "gbk"
    # print(resp2.text)
    result3 = obj3.search(resp2.text)
    movie = result3.group("movie")
    location = result3.group("location")
    link = result3.group("link")
    f.write(f"电影：{movie}\t产地：{location}\t下载链接：{link}\n")
f.close()
resp.close()
print("提取完毕")



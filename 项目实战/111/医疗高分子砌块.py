# 1.数据在哪
import pandas
import requests
import lxml.etree
product_list = []
for page in range(1,20):
    url = f'http://www.ntminyanmedical.com/products/17.html?page={page}&prop_filter=%7b%7d&listviewtype=table'
    # 2.身份
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','cookie':'kjsession=h0fg1cspieszv0m1d3q3mm32'}
    # 3.导入请求模块
    response = requests.get(url=url,headers=headers)
    # response = requests.request("", "", headers=headers)
    # 4.数据处理 方法html  导入lxml的模块
    html = lxml.etree.HTML(response.text) #使用lxml的子模块etree中的HTML功能
    # 这里计算机开始明白html格式，把文本变成这个格式
    chinese_names = html.xpath('/html/body/div[3]/div/div[2]/div[2]/div/ul/li[*]/div[1]/div/a/@title')  # li 列表 * 随便取
    english_name = html.xpath('/html/body/div[3]/div/div[2]/div[2]/div/ul/li[*]/div[1]/div/div[1]/span/text()')
    cas = html.xpath('/html/body/div[3]/div/div[2]/div[2]/div/ul/li[*]/div[1]/div/div[4]/span/text()')
    for i in range(len(chinese_names)):
        product = [chinese_names[i],english_name[i],cas[i]]  # 对应的数据放一起
        product_list.append(product)  # 得到的每条数据都放进列表里
# 翻页数据提取
# 5.保存
data = pandas.DataFrame(product_list) # Python中的列表结构-> 表格形式数据
data.to_excel('医药高分子砌块数据汇总表.xlsx', index=False, header=['中文名','英文名','cas'])
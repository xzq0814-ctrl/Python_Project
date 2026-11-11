from flask import Flask, render_template        # Flask 应用程序的后台框架 网络后台  渲染web网页
from flask_socketio import SocketIO, emit       # SocketIO 网络通信模块  广播通知
import datetime                                 # 时间模块
app = Flask(__name__)                 # 初始化创建一个app后台程序
app.config['SECRET_KEY'] = 'secret'   # 配置密码
socketio = SocketIO(app, cor_allowed_origins='') # 配置网络
# 主页路由 用户访问主页时 在这处理：返回index.html，提供页面
@app.route('/')
def index():
    return render_template('index.html')
# 有人进入聊天室
@socketio.on('join')
def handle_join(data):
    username = data['username']   # 提取用户名
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 通知
    emit(
        'user_joined',
        {'username': username, 'timestamp': timestamp, 'message':f'欢迎{username}加入群聊！'},
        broadcast=True)  # 给所有人发消息
# 有人发信息
@socketio.on('message')
def handle_message(data):
    username = data['username']  # 谁发
    message = data['message']    # 发啥
    timestamp = datetime.datetime.now().strftime('%H:%M')  # 啥时候
    emit(  # 通知给大家
        'message',
        {'username': username, 'timestamp': timestamp, 'message': message},
        broadcast=True)
# 启动后台，默认本机IP 端口号8888
# socketio.run(app, host='0.0.0.0', port=8888)
if __name__ == '__main__':
    socketio.run(
        app,
        host='0.0.0.0',
        port=8888,
        allow_unsafe_werkzeug=True,
        debug=True
    )





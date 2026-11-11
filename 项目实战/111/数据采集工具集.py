"""三个已完成采集脚本的统一入口（Python 3.9+）。

运行：python 数据采集工具集.py
依赖：python -m pip install requests lxml pandas openpyxl DrissionPage wordcloud matplotlib
评论采集还需要本机安装 Chrome 或 Edge，并按网页要求手动完成登录。
输出统一保存在本文件旁的“采集结果”目录中。原始脚本无需改动。
"""

import importlib
import json
import re
from contextlib import ExitStack
from datetime import datetime
from pathlib import Path


# 以脚本所在目录为基准，避免从其他工作目录启动时把结果保存到别处。
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / '采集结果'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/142.0.0.0 Safari/537.36'


def require(module, package=None):
    """按需导入并返回模块；缺少依赖时给出可直接执行的安装命令。

    module 是导入名，package 是可选的 pip 包名，例如 lxml.etree 对应 lxml。
    依赖在使用对应功能时才加载，未安装词云库不会影响音乐功能。
    """
    try:
        return importlib.import_module(module)
    except ImportError as exc:
        raise RuntimeError(f'缺少依赖，请安装：python -m pip install {package or module}') from exc


def ask_int(prompt, default, minimum=1, maximum=1000): # 提示输入值，并检测数据异常
    """循环读取范围内的整数；直接回车返回调用方给定的默认值。

    minimum、maximum 都包含在有效范围内；允许调用方将下限设为 0，
    用于“重新搜索”等菜单操作。默认值由调用方保证有效，不再单独校验。
    """
    while True:
        value = input(f'{prompt}（默认 {default}）：').strip()
        if not value:
            return default
        if value.isdecimal() and minimum <= int(value) <= maximum:
            return int(value)
        print(f'请输入 {minimum}～{maximum} 之间的整数。')


def safe_name(name):
    """替换 Windows 文件名中的非法字符，并避开系统保留名称。"""
    # 清理控制字符、末尾的点和空格，并限制名称长度，给时间戳和扩展名留空间。
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', str(name)).strip().rstrip('. ')[:120]
    name = name or '未命名'
    if name.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL', *[f'COM{i}' for i in range(1, 10)], *[f'LPT{i}' for i in range(1, 10)]}:
        name = '_' + name
    return name


def new_path(folder, name, suffix):
    """创建结果子目录，返回带时间戳的 Path；此时尚未创建结果文件。

    folder 为功能目录，name 为原始名称，suffix 为带点的扩展名（如 .xlsx）。
    所有结果统一放在 OUTPUT_DIR 下，名称经过 safe_name 清理。
    """
    directory = OUTPUT_DIR / folder
    directory.mkdir(parents=True, exist_ok=True)
    # 时间戳避免重复运行覆盖上一次采集结果。
    return directory / f'{safe_name(name)}_{datetime.now():%Y%m%d_%H%M%S_%f}{suffix}'


def make_session():
    """创建带统一浏览器标识的请求会话，供同一次任务复用连接。

    调用方使用 with 管理返回的 Session，任务结束或异常时释放连接资源。
    """
    requests = require('requests')
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})
    return session


def request(session, url, **kwargs):
    """统一设置超时并检查 HTTP 状态，避免错误页被当作正常数据。"""
    # 分别设置连接超时 10 秒、读取超时 30 秒；params、stream 等参数原样传递。
    response = session.get(url, timeout=(10, 30), **kwargs)
    try:
        response.raise_for_status()
    except Exception:
        response.close()
        raise
    # 成功响应交给调用方通过 with 关闭；失败响应已在上面的异常分支关闭。
    return response


def parse_products(html_text):
    """将 HTML 转为产品字典列表；无有效页面时返回空列表。

    新增容错：跳过缺少中文名的节点，英文名或 CAS 缺失时填空字符串，
    保证每条记录的三个字段始终属于同一个产品。
    """
    etree = require('lxml.etree', 'lxml')
    root = etree.HTML(html_text)
    if root is None:
        return []
    rows = []
    # 在每个产品节点内部提取字段，避免三组列表长度不一致导致数据错位。
    nodes = root.xpath('/html/body/div[3]/div/div[2]/div[2]/div/ul/li/div[1]')
    for node in nodes:
        names = node.xpath('./div/a/@title')
        if not names:
            continue
        english = node.xpath('./div/div[1]/span/text()')
        cas = node.xpath('./div/div[4]/span/text()')
        rows.append({'中文名': names[0].strip(),
                     '英文名': english[0].strip() if english else '',
                     'CAS': cas[0].strip() if cas else ''})
    return rows


def collect_products():
    """交互式选择采集页数，汇总产品并去重导出 Excel。

    新增空页停止和部分结果保存：后续请求失败或用户中断时，finally
    仍尝试导出已收集的数据；异常随后继续交给主菜单处理。
    """
    pandas = require('pandas')
    require('openpyxl')  # pandas写.xlsx(用来读写Excel文件)
    pages = ask_int('采集页数', 19)
    rows = []
    try:
        with make_session() as session:
            for page in range(1, pages + 1):
                with request(session, 'http://www.ntminyanmedical.com/products/17.html',
                             params={'page': page, 'prop_filter': '{}', 'listviewtype': 'table'}) as response:
                    current = parse_products(response.text)
                if not current:
                    print(f'第 {page} 页未提取到产品，停止翻页；请确认页面结构或访问状态。')
                    break
                rows.extend(current)
                print(f'第 {page} 页：{len(current)} 条。')
    finally:
        # 后续页面失败或用户中断时，也保存已经成功获取的数据。
        if rows:
            path = new_path('产品信息', '高分子砌块数据汇总', '.xlsx')
            data = pandas.DataFrame(rows).drop_duplicates()
            data.to_excel(path, index=False)
            print(f'已保存 {len(data)} 条产品：{path}')


def singer_name(song):
    """提取歌曲字典中的全部有效歌手名，用顿号连接；没有有效姓名时返回“未知”。"""
    names = [singer['name'].strip() for singer in (song.get('singers') or [])
             if isinstance(singer, dict) and isinstance(singer.get('name'), str)
             and singer['name'].strip()]
    return '、'.join(names) or '未知'


def download_audio(session, url, path):
    """流式下载音频至 Path 指定的位置，完成检查后再生成最终文件。

    文本响应或空内容会抛出 ValueError；下载或写入失败时异常向上传递，
    finally 尝试删除 .part 临时文件，避免把未完成内容当作成品。
    """
    # 分块写入临时文件，避免整首音乐常驻内存；下载成功后才改为最终文件名。
    temporary = path.with_suffix(path.suffix + '.part')
    try:
        with request(session, url, stream=True) as response:
            content_type = response.headers.get('Content-Type', '').lower()
            if any(kind in content_type for kind in ('text/', 'json', 'html')):
                raise ValueError('下载地址返回文本或错误信息，未保存为音频。')
            with temporary.open('wb') as handle:
                for chunk in response.iter_content(chunk_size=64 * 1024):
                    if chunk:
                        handle.write(chunk)
        if temporary.stat().st_size == 0:
            raise ValueError('下载内容为空。')
        # 只有响应完整读取且文件非空，才将临时文件移动为最终结果。
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def music_tool():
    """在同一会话中循环搜索、选歌和下载；输入 0 可返回或重新搜索。

    新增输入校验、空结果及缺少下载地址的提示；网络或下载异常由主菜单处理。
    搜索和获取下载地址的接口沿用原音乐脚本。
    """
    with make_session() as session:
        while True:
            keyword = input('请输入歌曲关键词（输入 0 返回主菜单）：').strip()
            if keyword == '0':
                return
            if not keyword:
                print('关键词不能为空。')
                continue
            # 使用 params 编码关键词，正确处理中文、空格和特殊字符。
            with request(session, 'https://c.musicapp.migu.cn/v1.0/content/search_all.do', params={
                'text': keyword, 'pageNo': 1, 'pageSize': 20, 'isCopyright': 1, 'sort': 1,
                'searchSwitch': json.dumps({'song': 1, 'album': 0, 'singer': 0, 'tagSong': 1, 'mvSong': 0, 'bestShow': 1})
            }) as response:
                payload = response.json()
            songs = (payload.get('songResultData') or {}).get('result') or []
            if not songs:
                print('没有搜索结果，或接口未返回歌曲列表。')
                continue
            for index, song in enumerate(songs, 1):
                print(f"{index}. {song.get('name', '未知歌曲')} — {singer_name(song)}")
            choice = ask_int('下载序号（0 重新搜索）', 0, 0, len(songs))
            if choice == 0:
                continue
            song = songs[choice - 1]
            with request(session, 'https://c.musicapp.migu.cn/MIGUM3.0/strategy/listen-url/v2.3',
                         headers={'channel': '0140210'}, params={
                             'copyrightId': song['copyrightId'], 'contentId': song['contentId'],
                             'resourceType': 2, 'albumId': '', 'netType': '01', 'toneFlag': 'PQ'
                         }) as response:
                payload = response.json()
            url = (payload.get('data') or {}).get('url')
            if not url:
                print('接口未提供可下载地址，请重新选择歌曲。')
                continue
            path = new_path('音乐', f"{song.get('name', '未知歌曲')}-{singer_name(song)}", '.mp3')
            download_audio(session, url, path)
            print(f'下载完成：{path}')


def create_wordcloud(text):
    """根据评论文本生成、保存并展示词云。

    新增字体路径检查、空文本检查和 PNG 保存；优先使用 Windows 微软雅黑，
    不存在时让用户指定字体。评论文本由采集流程提前保存，词云失败不会丢失文本。
    """
    wordcloud = require('wordcloud')
    pyplot = require('matplotlib.pyplot', 'matplotlib')
    font = Path('C:/Windows/Fonts/msyh.ttc')
    if not font.exists():
        font = Path(input('请输入中文字体文件的完整路径：').strip().strip('"'))
    if not font.is_file():
        raise ValueError('字体文件不存在，评论文本已保留。')
    cleaned = re.sub(r'\[.*?\]', '', text)
    if not cleaned.strip():
        print('清理后没有可用于生成词云的文本。')
        return
    # 延续原脚本的词云逻辑；此处没有增加中文分词或情感分析。
    cloud = wordcloud.WordCloud(font_path=str(font), width=1920, height=1080,
                               background_color='white').generate(cleaned)
    path = new_path('评论', '评论词云', '.png')
    cloud.to_file(str(path))
    print(f'词云已保存：{path}')
    pyplot.imshow(cloud, interpolation='bilinear')
    pyplot.axis('off')
    pyplot.show()
    pyplot.close()


def offer_wordcloud(texts):
    """采集正常结束后调用：有评论才询问，无评论直接返回。"""
    if not texts:
        return
    answer = input('是否生成并展示词云？[Y/n]：').strip().lower()
    # 提示中的大写 Y 表示默认同意，直接回车也生成词云。
    if answer != 'n':
        create_wordcloud('\n'.join(texts))


def save_comments(texts):
    """将非空评论列表以 UTF-8 逐行写入新文件；空列表不创建文件。

    作为 ExitStack 的清理回调使用，正常结束或异常退出时均会尝试保存。
    """
    if not texts:
        return
    path = new_path('评论', '视频评论', '.txt')
    path.write_text('\n'.join(texts), encoding='utf-8')
    print(f'已保存 {len(texts)} 条评论：{path}')


def collect_comments():
    """交互式监听评论响应，去重收集后保存文本，并可选生成词云。

    新增链接校验、监听批数上限、15 秒等待超时及响应格式检查。
    浏览器登录和评论加载仍由用户配合完成；退出时停止监听并保存已有评论。
    """
    drission = require('DrissionPage')
    url = input('请输入抖音视频链接（直接回车返回）：').strip()
    if not url:
        return
    if not url.startswith(('https://', 'http://')):
        raise ValueError('请输入以 http:// 或 https:// 开头的完整链接。')
    batches = ask_int('最多监听多少批评论', 50)
    page = drission.ChromiumPage()
    # texts 保留首次出现的顺序；seen 只记录去重键，供后续批次快速判断。
    texts, seen = [], set()
    # ExitStack 按注册的逆序执行清理：先停止监听，再保存评论。  可以清理打开的文件，异常处理
    # 即使采集或停止监听抛出异常，保存回调也会执行；异常仍交给主菜单处理。
    with ExitStack() as cleanup:
        cleanup.callback(save_comments, texts)
        page.get(url)
        input('请在浏览器中完成必要的登录，打开目标视频；准备好后按回车开始监听。')
        page.listen.start('comment/list')
        # 仅在监听成功启动后注册停止操作，避免未启动时调用 stop()。
        cleanup.callback(page.listen.stop)
        # 原页面的 CSS 类名可能变更，允许手动打开评论区后继续。
        button = page.ele('css:.jp8u3iov', timeout=3)
        if button:
            button.click()
        print('请打开或滚动评论区以触发请求；连续 15 秒无新响应将结束采集。')
        for _ in range(batches):
            packet = page.listen.wait(timeout=15)
            if not packet:
                print('没有收到新的评论响应，结束采集。')
                break
            payload = packet.response.body
            # 兼容浏览器库直接解析好的字典，以及尚未解析的 JSON 字符串或字节。
            if isinstance(payload, (str, bytes)):
                payload = json.loads(payload)
            if not isinstance(payload, dict):
                raise ValueError('评论响应不是预期的 JSON 对象。')
            for comment in payload.get('comments') or []:
                user = comment.get('user') or {}
                text = comment.get('text') or ''
                # 优先按评论 ID 去重，避免滚动时重复响应造成重复保存。
                key = comment.get('cid') or (user.get('sec_uid'), text)
                if not text or key in seen:
                    continue
                seen.add(key)
                texts.append(text)
                print(f"来自【{comment.get('ip_label', '未知')}】的【{user.get('nickname', '未知')}】说：{text}  主页：https://www.douyin.com/user/{user.get('sec_uid', '')}")
            if payload.get('has_more') in (0, False):
                # 服务端明确表示没有更多评论时提前结束，不继续等待剩余批次。
                break
            loading = page.ele('加载中', timeout=2)
            if loading:
                page.scroll.to_see(loading)
            else:
                print('请手动滚动评论区以加载下一批。')
    # 只有采集及清理正常结束，才询问是否生成词云。
    offer_wordcloud(texts)


def main():
    """统一菜单入口：按选项调用功能，并在任务失败或中断后继续显示菜单。"""
    # 字典中存放函数本身，用户选择有效序号后才执行对应任务。
    actions = {'1': collect_products, '2': collect_comments, '3': music_tool}
    while True:
        print('\n========== Python 数据采集工具集 ==========')
        print('1. 产品信息采集并导出 Excel\n2. 抖音评论采集与词云\n3. 音乐搜索与下载\n0. 退出')
        print(f'输出目录：{OUTPUT_DIR}')
        choice = input('请选择功能：').strip()
        if choice == '0':
            return
        action = actions.get(choice)
        if action is None:
            print('请输入菜单中的序号。')
            continue
        try:
            action()
        except KeyboardInterrupt:
            print('\n当前任务已中断，返回主菜单。')
        except Exception as exc:
            # 一个模块失败只结束本次任务，用户仍可选择其他模块。
            print(f'本次任务未完成：{type(exc).__name__}: {exc}')


if __name__ == '__main__':
    # 仅直接运行文件时启动菜单；在菜单输入阶段中断或遇到输入结束则退出程序。
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\n程序已退出。')

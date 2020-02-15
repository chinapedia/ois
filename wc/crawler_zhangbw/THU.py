from bs4 import BeautifulSoup
import requests
import re
import time
import json

MAX_NEWS = 10
HEADER = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.130 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_news():
    print('----------正在爬取----------')
    # 获取历史新闻

    history_file = open('history_news.json', 'r', encoding='utf-8')
    history_str = history_file.read()
    history_str = history_str.encode('utf-8')
    history_news = json.loads(history_str)
    history_file.close()
    # 获取网页
    THU_info = requests.get('http://news.tsinghua.edu.cn/publish/thunews/9648/index.html', headers=HEADER)
    THU_info.encoding = 'utf-8'

    # 解析网页
    soup = BeautifulSoup(THU_info.text, features='lxml')

    all_figure = soup.findAll('figure')[:MAX_NEWS]
    tmp = []  # 在一次性获取多个新闻时保持总的时间顺讯

    output_flag = False             # 判断是否有新增新闻
    for item in all_figure:
        try:
            link = item.findAll('a')[0]['href']
            title = item.findAll('a')[0].text
            abstract = re.findall(r'cutSummary\("(.*)",', item.findAll('p')[0].text)[0]  # 去除多余字符
        except IndexError:
            print('ERROR: Wrong format!')  # 格式异常
            return

        cur_news = [title, abstract, link]
        if cur_news not in history_news:  # 新闻更新
            tmp.append(cur_news)
            output_flag = True
            print('----------新增新闻----------')
            print('标题: %s\n摘要: %s\n链接: %s\n' % (cur_news[0], cur_news[1], cur_news[2]))

    if not output_flag:
        print('----爬取结束,没有新增新闻----\n\n')
        return
    history_news = tmp + history_news  # 保持新闻顺序
    if len(history_news) > MAX_NEWS:
        history_news = history_news[:MAX_NEWS]
    history_file = open('history_news.json', 'w', encoding='utf-8-sig')
    history_file.write(json.dumps(history_news))  # 输出到json文件保存
    history_file.close()
    print('----------爬取结束----------\n\n')


def output():
    history_file = open('history_news.json', 'r', encoding='utf-8')
    history_str = history_file.read()
    history_str = history_str.encode('utf-8')
    history_news = json.loads(history_str)
    history_file.close()
    for i in range(min(len(history_news), MAX_NEWS)):  # 输出到控制台
        print('----------第%s条新闻----------' % (i + 1))
        print('标题: %s\n摘要: %s\n链接: %s\n' % (history_news[i][0], history_news[i][1], history_news[i][2]))


if __name__ == '__main__':
    history = open('history_news.json', 'w', encoding='utf-8')      # 启动程序时重置历史记录
    history.write(json.dumps([]))
    history.close()
    while True:
        start = time.time()                     # 将程序时间算在内，保证5s刷新一次
        get_news()
        while time.time() < start + 5:
            pass

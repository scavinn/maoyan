import requests,re,json,time
from requests.exceptions import RequestException
from fake_useragent import UserAgent
from multiprocessing import Pool

ua = UserAgent()
headers = {'User-Agent':ua.random,}

def  get_one_page(url):
    '''
    请求榜单第一页，获取网页源码
    '''
    try:
        response = requests.Session().get(url,headers=headers)
        if response.status_code == 200:
            res = response.text
            return res
        return None
    except RequestException:
        return None

def parse_one_page(html):       #html=response.text
    '''
    用正则匹配，抓取电影相关信息
    '''
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">'
                         +'(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {                             #生成器，需要遍历
            'index':item[0],
            'title':item[1],
            'actor':item[2].strip()[3:],
            'time':item[3][5:],
            'score':item[4]+item[5]
        }

def write_to_file(content):
    '''
    写成json格式，导出到txt文本中
    '''
    with open('movie.txt','a',encoding='utf-8')as f:
        # content为字典形式，不能写入文件，需要用json.dumps写成json格式，用ensure_ascii指定utf-8不变，保持中文形式
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

#运行主程序
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)     # 构造多页函数
    html = get_one_page(url)
    # parse_one_page(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        time.sleep(1)
        main(i*10)
    # pool = Pool()         # 多进程
    # pool.map(main,[i*10 for i in range(10)])

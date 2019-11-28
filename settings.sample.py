# coding=utf-8
import logging

from colorama import Style
from colorama import init

# 设置log
logging.basicConfig(
    level=logging.INFO,
    format=''.join([Style.DIM, '[%(asctime)s] ',
                    Style.NORMAL, '%(message)s',
                    Style.RESET_ALL]),
    datefmt='%T',
)
logging.getLogger("requests").setLevel(logging.WARNING)

# 命令行
init(autoreset=True)

# 存储目录
STORE_PATH = './downloads'

# 每次请求数据的间隔（为避免频繁请求被封禁）
SLEEPTIME = 0

# 在这里粘贴你的cookies
COOKIES = 'SCF=...;SSOLoginState=...;SUB=...;SUHB=...'

# 爬取的照片翻页数目，默认设置为10000，表示全部爬取
MAX_PAGE = 10000

# 在这里添加目标用户的微博主页url
TARGETS = [
        #  'https://www.weibo.com/p/10080883d7b8a4ba9ca03c1e863198265ea9fa/topic_album?from=page_100808&mod=TAB#place'
        ]

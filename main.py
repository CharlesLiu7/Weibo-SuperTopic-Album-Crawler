# -*- coding: UTF-8 -*-
__author__ = 'Charles'
from bs4 import BeautifulSoup
import time
import urllib
import os
import sys
import gzip
import pickle
import logging
from colorama import Fore, Style
import settings
from weibo.api import WeiboApi
import socket


class Crawler(object):

    def __init__(self, target_url, MAX_PAGE):
        self.logger = logging.getLogger(__name__)
        self.MAX_PAGE = MAX_PAGE
        # 目标数据
        self.logger.info(Fore.GREEN + target_url)
        self.target = WeiboApi.fetch_user_info(target_url)
        self.page_id, self.title_value = self.target['page_id'], self.target['title_value']
        # 断点数据
        self.cpdir = './checkpoints/'
        if not os.path.isdir(self.cpdir):
            os.makedirs(self.cpdir)
        self.filename = self.page_id + '_resume.pkl.gz'
        self.sleeptime = settings.SLEEPTIME
        if os.path.isfile(os.path.join(self.cpdir, self.filename)):
            with gzip.open(os.path.join(self.cpdir, self.filename), 'rb') as f:
                self.since_id, self.page = pickle.load(f)
            self.logger.info(
                Fore.GREEN + 'Resuming from {0} with page={1}'.format(self.filename, self.page))
        else:
            self.since_id = ''
            self.page = 1  # Page starts from 1
            self.logger.info(
                Fore.GREEN + 'Starting from begining with page={0}'.format(self.page))
        self.root = self.__init_folder()

    def start(self):
        """开始下载图片缩略图和大图
        """
        flag = True
        while flag:
            self.logger.info(
                Fore.YELLOW + 'since_id={0}, page={1}'.format(self.since_id, str(self.page)))
            try:  # 有时候会解析失败
                r = WeiboApi.chaohua_img_info(
                    self.since_id, self.page_id, self.page)
                #  print(r.url)
                b = BeautifulSoup(r.json()['data'], features="lxml")
            except Exception as e:
                self.logger.error(
                    Fore.RED + 'since_id={0}, page={1}, err={2}'.format(self.since_id, self.page, e))
                with gzip.open(os.path.join(self.cpdir, self.filename), 'wb') as f:
                    pickle.dump(obj=[self.since_id, self.page], file=f)  # 保存现场
                sys.exit('Bye! Use `python main.py` to continue downloading.')
            for i in b.findAll('img'):
                uri = i.attrs['src']
                if 'http' not in uri:
                    uri = 'https:'+uri  # 有些URI头部没有HTTPS，加上
                #  print(uri)
                try:
                    uri_pair = {'thumbnail': uri,
                                'large': uri.replace('thumb300', 'large')}
                    for t in uri_pair:
                        time.sleep(self.sleeptime)
                        uri = uri_pair[t]
                        filename = os.path.join(
                            self.root, t+'/' + uri[uri.rfind('/')+1:])
                        if os.path.isfile(filename):
                            self.logger.info(Fore.BLUE + Style.DIM + filename)
                            continue
                        else:
                            urllib.request.urlretrieve(uri, filename)
                            self.logger.info(Fore.BLUE + filename)
                except KeyboardInterrupt:
                    self.logger.error(
                        Fore.RED + 'since_id={0}, page={1}, err=KeyboardInterrupt'.format(self.since_id, self.page))
                    with gzip.open(os.path.join(self.cpdir, self.filename), 'wb') as f:
                        pickle.dump(
                            obj=[self.since_id, self.page], file=f)  # 保存现场
                    sys.exit('Bye! Use `python main.py` to continue downloading.')
                except Exception as e:
                    self.logger.error(
                        Fore.RED + 'Img={0}, err={1}'.format(uri, e))

            # 模拟翻页
            flag = False
            for div in reversed(b.findAll('div')):
                # action-data 里的 since_id 是翻页的根据
                if 'action-data' in div.attrs:
                    tmp = div.attrs['action-data']
                    dic = dict([j.split('=')[0], j.split('=')[1]]
                               for j in tmp.split('&'))
                    if 'since_id' in dic and self.page < self.MAX_PAGE:
                        flag = True
                        self.since_id = urllib.parse.unquote(dic['since_id'])
                        self.page += 1
                        break
            if not flag:
                with gzip.open(os.path.join(self.cpdir, self.filename), 'wb') as f:
                    pickle.dump(obj=[self.since_id, self.page], file=f)  # 保存末尾
                self.logger.info(Fore.BLUE + 'Crawler finished')

    def __init_folder(self):
        """
        准备文件夹
        需要检测是否存在相同page_id、不同name的情况
        :return: str 该用户的存储文件夹名
        """
        # 根目录
        root = settings.STORE_PATH
        if not os.path.exists(root):
            os.mkdir(root)
        # 用户目录名
        home = '-'.join([self.page_id, self.title_value])
        home_path = os.path.join(root, home)
        # 处理更改微博名的情况
        for dir in os.listdir(root):
            if dir.startswith(self.page_id):
                if dir != home:
                    src = os.path.join(root, dir)
                    dst = os.path.join(root, home)
                    os.rename(src, dst)
                break
        else:  # 没有已知uid的文件夹
            os.mkdir(home_path)
            os.mkdir(os.path.join(home_path, 'thumbnail'))
            os.mkdir(os.path.join(home_path, 'large'))
        return home_path


if __name__ == '__main__':
    socket.setdefaulttimeout(30)
    for target in settings.TARGET:
        Crawler(target, settings.MAX_PAGE).start()

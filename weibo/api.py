# coding=utf-8
import json
import re
from time import time
import requests
import settings


class Url(object):
    ALBUM_LIST = 'http://photo.weibo.com/albums/get_all'
    PHOTO_IDS = 'http://photo.weibo.com/photos/get_photo_ids'
    LARGE_LIST = 'http://photo.weibo.com/photos/get_multiple'


class Pattern(object):
    CONFIG = re.compile(r"\$CONFIG\['(?P<key>.*)'\]='(?P<value>.*)';")


class Formatter(object):
    INDEX_URL = 'http://weibo.com/u/{uid}'.format
    LARGE_URL = '{host}/large/{name}'.format


def _load_cookies():
    """
    从设置中解析cookies
    :return: dict
    """
    assert settings.COOKIES, '请在`settings.py`中粘贴cookies'
    return dict([l.split('=') for l in settings.COOKIES.split('; ')])


class WeiboApi(object):
    """
    微博API
    访问流程: url -> id -> albums -> photo_ids(all) -> large_pics(batch)
    """

    COOKIES = _load_cookies()

    @staticmethod
    def get(*args, **kwargs):
        """
        添加了cookies的request.get的快捷方式
        :param args: see request.get
        :param kwargs: see request.get
        :return: request.Response
        """
        kwargs.setdefault('cookies', WeiboApi.COOKIES)
        return requests.get(*args, **kwargs)

    @staticmethod
    def get_json(*args, **kwargs):
        """
        获取response中的json数据的data域
        :param args: see get
        :param kwargs: see get
        :return: dict
        """
        return json.loads(WeiboApi.get(*args, **kwargs).text)['data']

    @staticmethod
    def fetch_user_info(url):
        """
        从任意用户的主页获取其相关数据
        :param url: 主页url
        :return: dict
        """
        content = WeiboApi.get(url).text
        return dict(Pattern.CONFIG.findall(content))

    @staticmethod
    def make_rnd():
        """
        生成__rnd参数
        :return: int
        """
        return int(time() * 1000)

    @staticmethod
    def chaohua_img_info(since_id, page_id, page):
        """ 获取当前瀑布流的图片信息
        """
        url = 'https://www.weibo.com/p/aj/proxy?api=http://i.huati.weibo.com/pcpage/papp'
        params = {
            'ajwvr': 6,
            'appname': 'album',
            'module': 'feed',
            'is_feed': 1,
            'page_id': page_id,
            'since_id': since_id,
            'page': page,
            '__rnd': WeiboApi.make_rnd(),
        }
        return WeiboApi.get(url, params)

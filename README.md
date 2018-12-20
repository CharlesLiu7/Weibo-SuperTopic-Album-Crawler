# Weibo Album SuperTopic Crawler 

![python](https://img.shields.io/badge/Python-3.7-brightgreen.svg)![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)

新浪微博超级话题相册爬虫。包含缩略图和大图

## Usage

1. 安装

    ```shell
    git clone https://github.com/CharlesLiu7/Weibo-SuperTopic-Album-Crawler
    cd Weibo-SuperTopic-Album-Crawler
    virtualenv env --python=python3
    source ./env/bin/activate
    pip install -r requirements.txt
	rm *.pkl.gz
    mv settings.sample.py settings.py
    ```

2. 设置`settings.py`

    * `STORE_PATH` 下载目录
    * `COOKIES` 任意用户微博的cookies，推荐包含以下字段 `SCF`, `SSOLoginState`, `SUB`, `SUHB`
    * `TARGETS` 目标超级话题的微博主页url

3. 运行

    `python main.py`

4. 注意: 有时候会解析失败，代码提供了断点保存功能在 `.pkl.gz` 文件中；程序因为抓取翻页结果失败退出后，可以直接重新运行以继续:

    ```shell
    python main.py
	```

	每次开始一个新的话题爬取之前请执行

    ```shell
	rm *.pkl.gz
    ```

## 感谢  Acknowledgement

感谢 [Lodour/Weibo-Album-Crawler](https://github.com/Lodour/Weibo-Album-Crawler) 提供的API和良好的代码结构，以及在 [Issue 12](https://github.com/Lodour/Weibo-Album-Crawler/issues/12) 中提出的良好建议。

## License

MIT License

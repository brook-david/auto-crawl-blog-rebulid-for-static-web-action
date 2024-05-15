from pathlib import Path

import scrapy
import logging
from typing import TYPE_CHECKING, Any, Iterable, List, Optional, Union, cast


class QuotesSpider(scrapy.Spider):
    # 爬虫名 启动爬虫 scrapy crawl blog
    name = "blog"
    # 下载域名
    downloadHost = "blog.wanderto.top"
    # 保存目录
    saveDir = "."
    # 已访问列表
    accessedList = []
    # 已下载列表
    downloadedList = []
    # 爬取开始地址
    start_urls = [
        "https://blog.wanderto.top",
    ]

    def parse(self, response):
        self.log("访问pares:" + response.url)
        # 添加到已访问集合
        self._addAccess(response.url)
        # 下载当前页面
        self.download(response)

        # 资源下载
        # 图片下载
        images = response.css("img::attr(src)")
        self.log("images :" + str(images))
        for item in images:
            s_item = str(item)
            if s_item.__contains__(self.downloadHost) and not self._isDownloaded(s_item):
                yield response.follow(s_item, self.download)
        # link(css)下载
        links = response.css("link::attr(href)")
        self.log("links :" + str(links))
        for item in links:
            # 移除url后的参数
            s_item = self._removeParameter(str(item))
            if s_item.__contains__(self.downloadHost) and not self._isDownloaded(s_item):
                yield response.follow(s_item, self.download)
        # script下载
        scripts = response.css("script::attr(src)")
        self.log("scripts :" + str(scripts))
        for item in scripts:
            # 移除url后的参数
            s_item = self._removeParameter(str(item))
            if s_item.__contains__(self.downloadHost) and not self._isDownloaded(s_item):
                yield response.follow(s_item, self.download)

        # 其他页面爬取
        aList = response.css("a::attr(href)")
        self.log("")
        for a in aList:
            stra = str(a)
            if stra.__contains__(self.downloadHost):
                if self._isAccessed(stra):
                    self.log("已下载过的本站地址：" + stra)
                    continue

                self.log("可下载的本站地址："+stra)
            else:
                self.log("不可下载的地址：" + stra)
                continue
            yield response.follow(a, self.parse)

    def download(self, response):
        self._download(response.url, response.body)
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)

    def _download(self, url, body):
        if self._isDownloadedAndSave(url):
            return
        # https://blog.wanderto.top/xx/xx/
        url = self._switchHtml(url)
        # self.log("进行页面下载流程，下载文件："+url)

        # 获取https://后的内容
        paths = url.split("/")[2:]
        if paths[0].__eq__(self.downloadHost):
            self.log("下载页面：" + url)
        else:
            return

        # 去除host
        paths = paths[1:]

        for index, name in enumerate(paths):
            path = self._getMainDir() + "/" + "/".join(paths[0:index + 1])
            file = Path(path)
            if name.__eq__(paths[-1]):
                # self.log("file:" + name)
                if file.exists():
                    self.log("warn: file exists " + path)
                    continue
                file.write_bytes(body)
            else:
                # self.log("dir:" + name)
                if file.exists():
                    continue
                file.mkdir()

    def _getMainDir(self):
        dir = Path(self.saveDir)
        if not dir.exists():
            dir.mkdir()
        return self.saveDir

    def _switchHtml(self, url):
        # /与host结尾则为页面
        if url.endswith("/"):
            url = url + "index.html"
        elif url.endswith(self.downloadHost):
            url = url + "/index.html"
        return url

    def _isDownloaded(self, url):
        if url in self.downloadedList:
            return True
        return False

    def _isDownloadedAndSave(self, url):
        if self._isDownloaded(url):
            return True
        self.downloadedList.append(url)
        return False

    def _isAccessed(self, url):
        if url in self.accessedList:
            return True
        return False

    def _addAccess(self, url):
        if not self._isAccessed(url):
            self.accessedList.append(url)

    def _removeParameter(self, url):
        return url.split("?")[0]

    def log(self, message: Any, level: int = logging.DEBUG, **kw: Any) -> None:
        print(message)


if __name__ == '__main__':
    q = QuotesSpider();
    # q._download(q.downloadHost, b"aa")
    # print(q._isDownloadedAndSave(q.downloadHost))
    # print(q._removeParameter(q.downloadHost+"/wp-content/plugins/enlighter/cache/enlighterjs.min.css?ver=vo/Yz0k1HSy0Sr5"))
    print(q.downloadHost+"/2024/04/28/wordpress-custome-css-define-website/".split("/"))

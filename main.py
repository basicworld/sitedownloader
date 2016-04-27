# -*- coding:utf8 -*-
"""
Usage:
  rabbit.py -u <url> [-d <delaytime>] [-o <save_dir>]

Arguments:
  delaytime     dirpath
  save_dir        fullpath to save your webpage
  url           url

Options:
  -h --help     show this help
  -d            delaytime
  -o            save_dir
  -u            url
"""
from docopt import docopt
# main.py -d 60 -u http://m.sohu.com -o /tmp/backup
import requests
import os
from datetime import datetime
from lxml import etree
from purl import URL
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# use for debug
proxies = {
    'http': 'http://127.0.0.1:8888',
    'https': 'http://127.0.0.1:8888',
}

# chrome header
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;\
        q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/50.0.2661.87 Safari/537.36',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
}


def xurljoin(base, url):
    """
    xurljoin(base, url)
    improved func for uelpsrse.urljoin
    article from: http://www.coder4.com/archives/2674
    @base   baseurl
    @url    path
    """
    from urlparse import urljoin
    from urlparse import urlparse
    from urlparse import urlunparse
    from posixpath import normpath

    url = url if url else ''
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path,
                       arr.params, arr.query, arr.fragment))


class SiteDownload(object):
    def __init__(self, url, save_dir='tmp'):
        """
        @url: full url of a site
        @save_dir: dir to save site
        """
        save_time = datetime.strftime(datetime.now(), '%Y%m%d%H%M')
        self.orig_dir = os.path.join(save_dir, save_time)
        self.save_dir = os.path.abspath(os.path.join(save_dir, save_time))
        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

        self.url = url
        u = URL(url)
        self.host = u.scheme() + '://' + u.host()
        print self.host, save_time

    def get_html(self):
        """"""
        resp = requests.get(self.url,
                            headers=headers,
                            allow_redirects=False,
                            verify=False,
                            stream=True)
                            # proxies=proxies)
        if resp.ok:
            self.html = resp.content.lower().decode('utf8')
        self.tree = etree.HTML(self.html)

    def get_css(self):
        """
        css_file is in <link>
        """
        css_dir = os.path.join(self.save_dir, 'css')
        os.makedirs(css_dir) if not os.path.isdir(css_dir) else None

        css_nodes = self.tree.xpath('//link[@type="text/css"]')
        for node in css_nodes:
            css_url = node.attrib.get('href')
            if css_url:
                resp = requests.get(css_url,
                                    headers=headers,
                                    allow_redirects=False,
                                    verify=False, )
                                    # proxies=proxies)
                if resp.ok:
                    css_name = os.path.join(css_dir, os.path.basename(css_url))
                    with open(css_name, 'w') as f:
                        f.write(resp.content)
                    # replace css link
                    self.html = self.html.replace(css_url, css_name)

    def get_img(self):
        """"""
        img_dir = os.path.join(self.save_dir, 'images')
        os.makedirs(img_dir) if not os.path.isdir(img_dir) else None
        img_nodes = self.tree.xpath('//img')
        for node in img_nodes:
            original_img_url = node.attrib.get('original')
            src_img_url = node.attrib.get('src')
            img_url = original_img_url if original_img_url else src_img_url
            if img_url:
                original_img_url = img_url
                img_url = 'http:' + img_url if img_url.startswith('//') \
                    else img_url
                resp = requests.get(img_url,
                                    headers=headers,
                                    allow_redirects=False,
                                    verify=False,
                                    stream=True)
                                    # proxies=proxies)
                if resp.ok:
                    img_name = os.path.join(img_dir, os.path.basename(img_url))
                    try:
                        with open(img_name, 'wb') as f:
                            f.write(resp.content)
                    except IOError as e:
                        pass
                    # print src_img_url
                    # self.html = self.html.replace(src_img_url, img_name)
                    old = src_img_url + '" original="' + original_img_url
                    new = img_name + '" original="' + img_name
                    self.html = self.html.replace(old, new)
        pass

    def get_js(self):
        """"""
        js_dir = os.path.join(self.save_dir, 'js')
        os.makedirs(js_dir) if not os.path.isdir(js_dir) else None
        js_nodes = self.tree.xpath('//script')
        for node in js_nodes:
            js_url = node.attrib.get('src')
            if js_url:
                resp = requests.get(js_url,
                                    headers=headers,
                                    allow_redirects=False,
                                    verify=False, )
                                    # proxies=proxies)
                if resp.ok:
                    js_name = os.path.join(js_dir, os.path.basename(js_url))
                    with open(js_name, 'w') as f:
                        f.write(resp.content)
                    self.html = self.html.replace(js_url, js_name)

    def complete_url(self):
        """complete relative url in html"""
        a_nodes = self.tree.xpath('//a')
        for node in a_nodes:
            href = node.attrib.get('href')
            if href and not href.startswith('http') and \
                    not href.startswith('//'):
                print href, xurljoin(self.host, href)
                self.html = self.html.replace(href, xurljoin(self.host, href))

    def save_html(self):
        """"""
        with open(os.path.join(self.save_dir, 'index.html'), 'w') as f:
            f.write(self.html)

    def run(self):
        """"""
        self.get_html()
        self.get_css()
        self.get_img()
        self.get_js()
        self.complete_url()
        self.save_html()


def loop(url, save_dir='tmp', delaytime=None):
    """
    @url
    @delaytime: second to loop
    @save_dir
    """
    delaytime = int(delaytime) if (delaytime and delaytime.isdigit()) else None
    while True:
        sd = SiteDownload(url)
        sd.run()
        if not delaytime:
            break
        print('Sleep for %s second' % delaytime)
        time.sleep(delaytime)


def cmd():
    """
    function: command line
    """
    args = docopt(__doc__)
    print args

if __name__ == '__main__':
    loop('http://m.sohu.com/', 'tmp/backup', '')

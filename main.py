# -*- coding:utf8 -*-
"""
Usage:
  main.py -d <delaytime> -u <url>  [-o <save_dir>]

Arguments:
  delaytime     delaytime, eg: 60
  save_dir      path to save your site, eg: 'tmp'
  url           url, eg: http://m.sohu.com

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
import re
import chardet
reload(sys)
sys.setdefaultencoding('utf8')
# disable ssl warning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
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
    from purl import URL

    url = url if url else ''
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = URL(arr[2]).path()
    return urlunparse((arr.scheme, arr.netloc, path,
                       arr.params, arr.query, arr.fragment))


class SiteDownload(object):
    def __init__(self, url, save_dir='tmp'):
        """
        @url: full url of a site
        @save_dir: dir to save site
        """
        save_time = datetime.strftime(datetime.now(), '%Y%m%d%H%M')
        self.save_time = save_time
        self.save_dir = os.path.abspath(os.path.join(save_dir, save_time))
        # create dir if not exist
        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

        self.url = url
        u = URL(url)
        # get host like: http://m.sohu.xom
        self.host = u.scheme() + '://' + u.host()
        # print self.host, save_time

    def get_html(self):
        """get html content"""
        resp = requests.get(self.url,
                            headers=headers,
                            # allow_redirects=False,
                            verify=False,
                            stream=True)
        if resp.ok:
            fencoding = chardet.detect(resp.content)

            # deal with encoding problem
            try:
                encoding = fencoding.get('encoding')
                encoding = encoding if encoding else 'utf8'
                self.html = resp.content.decode(encoding).encode('utf8')
            except UnicodeDecodeError as e:
                encoding = 'gbk' if fencoding.get('encoding').lower()\
                    in ('gb2312', ) else 'gb2312'
                self.html = resp.content.decode(encoding).encode('utf8')

            # change all encoding to utf-8
            pat = 'content="text/html; charset=.*?"'
            # must be utf-8 not utf8
            repl = 'content="text/html; charset=utf-8"'
            self.html = re.sub(pat, repl, self.html)
        else:
            raise TypeError('Something wrong when open %s' % self.url)
        self.tree = etree.HTML(self.html)

    def get_css(self):
        """
        css_file is in <link>
        """
        # create dir
        css_dir = os.path.join(self.save_dir, 'css')
        os.makedirs(css_dir) if not os.path.isdir(css_dir) else None

        css_nodes = self.tree.xpath('//link[@type="text/css"]')
        for node in css_nodes:
            # url is in attrib: href
            css_url = node.attrib.get('href')
            if css_url:
                old_css_url = css_url  # will be replaced by new_css_url
                # get full url
                css_url = xurljoin(self.host, css_url)

                # deal with special url: //a/b...
                css_url = 'http:' + css_url if css_url.startswith('//')\
                    else css_url
                resp = requests.get(css_url, headers=headers,
                                    allow_redirects=False, verify=False)\
                    if css_url.startswith('http') else None
                if resp and resp.ok:
                    # base filename
                    base_name = os.path.basename(css_url)
                    # new pull filename
                    new_css_name = os.path.join('css', base_name)

                    # save file
                    try:
                        with open(os.path.join(css_dir, base_name), 'w') as f:
                            f.write(resp.content)
                        self.html = self.html.replace(old_css_url,
                                                      new_css_name)
                    except IOError as e:
                        pass

    def get_img(self):
        """save imgs to images<dir>"""
        img_dir = os.path.join(self.save_dir, 'images')
        os.makedirs(img_dir) if not os.path.isdir(img_dir) else None

        # lxml
        img_nodes = self.tree.xpath('//img')
        for node in img_nodes:
            ori_img_url = node.attrib.get('original')
            src_img_url = node.attrib.get('src')
            img_url = ori_img_url if ori_img_url else src_img_url
            if img_url:
                old_img_url = img_url
                img_url = xurljoin(self.host, img_url)
                img_url = 'http:' + img_url\
                    if img_url.startswith('//') else img_url
                # print img_url
                resp = requests.get(img_url, headers=headers,
                                    # allow_redirects=False,
                                    verify=False, stream=True)\
                    if img_url.startswith('http') else None

                if resp and resp.ok:
                    img_url = resp.url  # debug for redirect url
                    base_name = os.path.basename(img_url)
                    new_img_name = os.path.join('images', base_name)\
                        .replace('\\', '/')
                    try:
                        with open(os.path.join(img_dir, base_name), 'wb') as f:
                            f.write(resp.content)
                            f.close()
                        old = src_img_url + '" original="' + old_img_url
                        if old in self.html:
                            new = new_img_name + '" original="' + new_img_name
                            self.html = self.html.replace(old, new)
                        else:
                            self.html = self.html.replace(src_img_url,
                                                          new_img_name)
                    except IOError as e:
                        pass

        # # re
        # pat = '<img.*?src=\"(?P<src_url>.*?)\".*?>'
        # print re.findall(pat, self.html)
        # # <img src="images/30adcbef76094b363129fc07a5cc7cd98c109da5.jpg"

    def get_js(self):
        """save js to js<dir>"""
        js_dir = os.path.join(self.save_dir, 'js')
        os.makedirs(js_dir) if not os.path.isdir(js_dir) else None
        js_nodes = self.tree.xpath('//script')
        for node in js_nodes:
            js_url = node.attrib.get('src')
            if js_url:
                # print js_url
                old_js_url = js_url
                js_url = xurljoin(self.host, js_url)
                js_url = 'http:' + js_url if js_url.startswith('//') else \
                    js_url
                resp = requests.get(js_url, headers=headers,
                                    allow_redirects=False, verify=False, ) if \
                    js_url.startswith('http') else None
                                    # proxies=proxies)
                if resp and resp.ok:
                    base_name = os.path.basename(js_url)
                    js_name = os.path.join('js', base_name)
                    try:
                        with open(os.path.join(js_dir, base_name), 'w') as f:
                            f.write(resp.content)
                        self.html = self.html.replace(old_js_url, js_name)
                    except IOError as e:
                        pass

    def replace_other_relative_url(self):
        """replace relative url to full_url in html"""
        self.tree = etree.HTML(self.html)
        a_nodes = self.tree.xpath('//a')
        for node in a_nodes:
            href = node.attrib.get('href')
            if href and (not href.startswith('http')) and \
                    (not href.startswith('//')):
                # print href, xurljoin(self.host, href)
                old_href = 'href="%s"' % href
                new_href = 'href="%s"' % xurljoin(self.host, href)
                self.html = self.html.replace(old_href, new_href)

    def save_html(self):
        """save html to index.html"""
        with open(os.path.join(self.save_dir, 'index.html'), 'w') as f:
            f.write(self.html)

    def run(self):
        """control functions above"""
        self.get_html()
        self.get_css()
        self.get_img()
        self.get_js()
        self.replace_other_relative_url()
        self.save_html()
        return True
        # return {
        #     'ok': True,
        #     'save_dir': self.save_dir,
        #     'html': self.html,
        # }  # can be used for further function


def loop(url, save_dir, delaytime=None):
    """

    @url: full url needed
    @delaytime: second to loop.
     run sitedownload for every $delaytime second if not null
    @save_dir: dir to save site
    """
    delaytime = int(delaytime) if (delaytime and delaytime.isdigit()) else None
    while True:
        sd = SiteDownload(url, save_dir)
        resp = sd.run()
        if resp:
            main_html = sd.html
            main_save_dir = sd.save_dir
            tree = etree.HTML(main_html)
            sub_count = 0
            for node in tree.xpath('//a'):
                sub_save_dir = os.path.join(main_save_dir, 'subs',
                                            'sub%s' % sub_count)
                sub_url = node.attrib.get('href')
                if sub_url and sub_url.startswith('http'):
                    try:
                        sub_sd = SiteDownload(sub_url, sub_save_dir)
                        new_sub_url = os.path.join('subs',
                                                   'sub%s' % sub_count,
                                                   sub_sd.save_time,
                                                   'index.html')\
                            .replace('\\', '/')
                        sub_sd.run()
                        old_href = 'href="%s"' % sub_url
                        if old_href in main_html:
                            new_href = 'href="%s"' % new_sub_url
                            main_html = main_html.replace(old_href, new_href)
                    except ValueError as e:
                        pass
                sub_count += 1
                # just for a demo
                if sub_count > 15:
                    break
            with open(os.path.join(sd.save_dir,
                      'detail_index.html'), 'w') as f:
                f.write(main_html)

        if not delaytime:
            break
        print('Sleep for %s second' % delaytime)
        time.sleep(delaytime)


def cmd():
    """
    function: command line
    """
    args = docopt(__doc__)
    # print args
    if args.get('-u') and args.get('<url>').startswith('http'):
        save_dir = args.get('<save_dir>')
        save_dir = save_dir if save_dir else 'tmp'
        loop(args.get('<url>'), save_dir, args.get('<delaytime>'))
    else:
        raise TypeError('Wrong url %s' % args.get('<url>'))

if __name__ == '__main__':
    # loop('http://m.sohu.com/', 'tmp/backup', '')
    cmd()

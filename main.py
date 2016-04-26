# -*- coding:utf8 -*-
"""
Usage:
  rabbit.py -u <url> [-d <delaytime>] [-o <path>]

Arguments:
  delaytime     dirpath
  folder          fullpath to save your webpage
  url           url

Options:
  -h --help     show this help
  -d            delaytime
  -o            folder
  -u            url
"""
from docopt import docopt
# main.py -d 60 -u http://m.sohu.com -o /tmp/backup


def cmd():
    """
    function: command line
    """
    args = docopt(__doc__)
    print args

if __name__ == '__main__':
    cmd()

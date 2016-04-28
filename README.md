# sitedonload

python site downloader: save html, css, img and js for given url

fell free to contact me if you have any idea about this project：basicworld@163.com

python 网页下载器，用于下载html、css、img、js，支持`子网页下载`、`定时下载`、`命令行操作`、`日志记录`



	#eg
	python main.py -d '' -u http://m.sohu.com -o tmp


the site will be saved in following structure:

	$save_dir
	|-- sitelog.log
	|-- $save_time/
	    |-- index.html
	    |-- css/
	        |-- *.css
	    |-- images/
	        |--*.jpg/png/gif/ico
	    |-- js/
	        |-- *.js
		|-- subs/ (when use `-s` command)
			|-- sub0/
				|-- sitelog.log
				|-- $save_time
				    |-- index.html
				    |-- css/
				    |-- images/
				    |-- js/
			|-- sub1/

for each url, follwing content will be saved:

- log save in `sitelog.log`
- main page save in `index.html`
- css save in `css/`
- img save in `images/`
- javascript save in `js/`
- sub page save in `subs/` 

**Note**:

Ads not include 

this project runs well in: 

- 手机搜狐网 http://m.sohu.com
- qq新闻 http://news.qq.com/
- 知乎精华 https://www.zhihu.com/topic/19550228/top-answers

you may need to change code for your sepcific site, dont worry, its easy

	# eg for img url 
	original img_url in douban.com is in <img data-origin=""
	you just need to replace <img src="" to your image path

`Chrome` is recommanded to open index.html

coding in line with `pep8`

----
### before use

1. python version 2.7x required

2. you should install packages in file `dependence`

    pip install -r dependence

Note that some packages is not easy to install, eg lxml.
you should google for method

----
### how to use

**cmd**:

	Usage:
	  main.py -d <delaytime> -u <url>  [-o <save_dir>] [-s]

	Arguments:
	  delaytime     delaytime, eg: 60
	  save_dir      path to save your site, eg: 'tmp'
	  url           url, eg: http://m.sohu.com

	Options:
	  -h --help     show this help
	  -d            delaytime
	  -o            save_dir
	  -s            save sub urls
	  -u            url

    # eg
	# save http://m.sohu.com to `tmp/backup`
    python main.py -d '' -u http://m.sohu.com -o tmp/backup

	# save http://m.sohu.com to `tmp/backup` for every 60 seconds
    python main.py -d 60 -u http://m.sohu.com -o tmp/backup

	# save http://m.sohu.com and top 20 sub_urls to `tmp/backup` for every 60 seconds
    python main.py -d 60 -u http://m.sohu.com -o tmp/backup -s

    python main.py -d 60 -u http://www.sina.com.cn -o tmp/backup


**api**:

    from main import loop
    # loop(url, save_dir, delaytime=None)
    # eg, note that delaytime must be int_type_str

	# save http://m.sohu.com to `tmp/backup` for every 60 seconds
    loop('http://m.sohu.com', 'tmp', '60')

	# save http://m.sohu.com and top 20 sub_urls to `tmp/backup` for every 60 seconds
    loop('http://m.sohu.com', 'tmp', '60', True)

----

### todo

- multiprocessing support (需要进程间通讯，待验证)

----
### history

- add header to act as pc
- add loop() for sleep function
- add cmd using `docopt`
- debug: xurljoin() wrong when facing with `/?`: http://m.sohu.com/?...
- debug: special img_url in m.sohu.com: has both src and original
- debug: special img_url in m.sohu.com: src in same
- debug: special url like //a/b...
- debug: encoding problem appeared in 163.com
- debug: gb2312, gbk UnicodeDecodeError
- debug: wrong encoding when open with IE
- debug: convert some relative urls to abs urls
- debug: img url might be redirected
- debug: `\\` causes problem in url
- debug: ssl warning
- add function for zhihu.com: save png in <link>
- add command `-s`: use `-s` to save top 20 sub urls
- add log function: now you can check `sitelog.txt` for error info

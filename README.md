# sitedonload
save html, css, img and js for giving url

	main.py -d <delaytime> -u <url>  [-o <save_dir>] [-s]

the site will be saved in following structure:

    $save_time/
    |-- index.html
    |-- css/
        |-- *.css
    |-- images/
        |--*.jpg/png/gif/ico
    |-- js/
        |-- *.js
	|-- subs/ (when use `-s` command)
		|-- sub0/
			|-- $save_time
			    |-- index.html
			    |-- css/
			    |-- images/
			    |-- js/
		|-- sub1/

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
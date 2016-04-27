# sitedonload
save html, css, img and js

the site will be saved in following structure:

    $save_time
    |-- index.html
    |-- css
        |-- *.css
    |-- images
        |--*.jpg/png/gif/ico
    |-- js
        |-- *.js


`Chrome` is recommanded to open index.html

coding in line with `pep8`

### before use

1. python version 2.7x required

2. you should install packages in file `dependence`

    pip install -r dependence

Note that some packages is not easy to install, eg lxml.
you should google for method


### how to use

cmd:

    python  main.py -d <delaytime> -u <url>  [-o <save_dir>]
    # eg
    python main.py -d 60 -u http://m.sohu.com -o tmp/backup
    python main.py -d 60 -u http://www.sina.com.cn -o tmp/backup


api:

    from main import loop
    loop(url, save_dir, delaytime=None)
    # eg, note that delaytime must be int_type_str
    loop('http://m.sohu.com', 'tmp', '10')

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
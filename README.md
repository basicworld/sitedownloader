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

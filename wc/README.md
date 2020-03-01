
# Formated Data source

Formated data is the blood for machine learning & web services

* Public/private API & dataset
    * API: https://developer.twitter.com/
    * Google Dataset Search: https://datasetsearch.research.google.com/
    * Kaggle: https://www.kaggle.com/datasets
    * Example: ncov2019 https://github.com/joyqi/ncov2019
* Crawled in-house dataset
    * [robots.txt](https://en.wikipedia.org/wiki/Robots_exclusion_standard)
    * RSS
    * Parse HTML
    * Label data with conditional filters: opinions label https://www.nytimes.com/section/opinion
    * Examples: Bing Twitter answer, [@HuazhongUST](https://twitter.com/huazhongust) & 
 [HUST.py](https://bitbucket.org/liruqi/social/src/master/tools/getAccountLocation/spider/HUST.py), [@TestFlightX](https://twitter.com/testflightx)

# Crawling Mobile App
* Crawl from App UI: XML, http://appium.io/
* App network traffic & notification reverse engineering

# Homework
Choose one task you interested, and create a PR to bitbucket repo (recommend) or send your code to my email: ruqli@outlook.com.

* Create a Telegram News bot for your University like https://t.me/s/HuazhongUST, and create a [telegram bot](https://core.telegram.org/bots) to post news to group https://t.me/webspidering. If you are unable to reach open telegram in China, just output news title and url to console. You could refer to [HUST.py](https://bitbucket.org/liruqi/social/src/master/tools/getAccountLocation/spider/HUST.py).
* Crawl socks5 proxies from websites like http://spys.one/en/socks-proxy-list/ , output proxies to a text file, one proxy per line. You could refer to [this script](https://bitbucket.org/liruqi/mumevpn.com/src/master/socks_check.sh).

# Homework guides
Common issues:
* Content de-duplicate
* Schedule crawling job, crawl frequency

## News bot

Software enginnering:
* reusing code
* seperate config, confidencial and data from source code.

## Proxies bot
* Choose target site, e.g., http://31f.cn/socks-proxy/ is not updating.
* JavaScript emulator
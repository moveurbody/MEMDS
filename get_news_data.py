# -*- coding: utf-8 -*-
# @Time    : 2017/9/11 上午11:07
# @Author  : Yuhsuan
# @File    : news_data.py
# @Software: PyCharm Community Edition

# 根據某個檔案內的所有新聞路徑將其資料抓取出來後存擋

from newspaper import Article,fulltext
import requests
from lxml import html
import os
import time
import datetime
from log_module import log

def news_extract(news_url,name=None,source=None):
    log('[news_extract][start]')
    log('name: %s, source: %s, url: %s' % (name,source,news_url))
    try:
        if name == None:
            name = 'test'

        if source == None:
            source = 'test'

        log('[news_extract] URL: %s' % news_url)
        article = Article(news_url, fetch_images=False,)
        log('[news_extract] downloading')
        article.download()
        for i in range(10):
            try:
                article.parse()
                break
            except:
                time.sleep(5)
        log('[news_extract] parsing')
        article.parse()
        time.sleep(3)
        log('[news_extract] inserting')
        # article.build()
        new_content = article.text
        new_content = new_content.strip().split('\n\n')
        text = '\n'.join(new_content)
        text = text.strip()

        authors = article.authors
        date = article.publish_date
        date  = datetime.datetime.strftime(date, '%Y%m%d %H%M%S.txt')
        title = article.title

        # 避免重複的日期
        file_name = date
        for i in range(9):
            if not os.path.exists(os.curdir+'/%s/%s/' % (source,name)+file_name):
                break
            else:
                file_name = file_name[:14]+str(i)+file_name[15:]

        with open(os.curdir+'/%s/%s/' % (source,name) +file_name,'a+') as file:
            file.writelines(text)
        # article.nlp()
        # summary = article.summary
        # print(text)
        # print("========================================================")
        # print(summary)
        # print("========================================================")
        # print(article.meta_data)
        # #
        # print(title)
        # print(authors)
        result = []
        result.append(file_name)
        result.append(title)
        result.append(news_url)
        log('[news_extract] result: %s' % result)
        log('[news_extract][end]\n')
        return result
    except Exception as e:
        log('Error found: %s\nMessage: %s' % (news_url,e),lvl='W')
        log('[news_extract][end]\n')
        return False

if __name__ == '__main__':
    url = []
    temp = []

    # file_list = ['hk','sewol','crimea','test']
    file_list = ['brexit','catalan','crimea','gravitational','hk','missile','sewol','syria','turkish']
    sources = ['CNN','NewYorkTimes','Theguardian']

    for folder in file_list:
        for source in sources:
            if os.path.exists(os.curdir+'/%s/%s/%s_title.txt' % (source,folder,folder)):
                log('pass %s,%s' % (source,folder))
                pass
            else:
                log('start: %s,%s\n' % (source, folder))
                with open(os.curdir+'/%s/%s/%s_title_temp_full.txt' % (source,folder,folder)) as urls:
                    for line in urls.readlines():
                        # print(line)
                        url.append(line.strip())

                for i in url:
                    log(i)
                    res = news_extract(i,name=folder,source = source)
                    if res != False:
                        temp.append(res)

                temp.sort()

                log('write file')
                for lines in temp:
                    with open(os.curdir+'/%s/%s/%s_title.txt' % (source,folder,folder),'a+') as file:
                        file.writelines(lines[0]+'   '+lines[1]+'   '+lines[2]+'\n')
import re
import requests
from lxml.html import etree
import pandas as pd

id_pattern = re.compile('data-article-id="(.*?)">')
title_pattern = re.compile('<title>(.*?) - PubMed</title>')
page_max = int(input('需要爬多少页'))
find_title = input('检索关键词')
find_abstract = input('摘要关键词，多个词组之间用英文逗号分隔').split(',')
# page_max, find_title, find_abstract = 10, 'deep learning turbine', 'deep learning,computer vision'
L = []
for page in range(1, page_max + 1):
    print('第{}页'.format(page))
    url = 'https://pubmed.ncbi.nlm.nih.gov/?term={}&page={}'.format(find_title.replace(' ', '+'), page)
    r = requests.get(url)
    data = id_pattern.findall(r.text)
    if not data:
        break
    for i in data:
        url_article = 'https://pubmed.ncbi.nlm.nih.gov/{}/'.format(i)
        r_article = requests.get(url_article)
        html = etree.HTML(r_article.text)
        title = (title_pattern.findall(r_article.text))[0]
        print(title)
        abs_xpaths = html.xpath('//*[@id="abstract"]/div/*')
        Abs = ''
        for abs_xpath in abs_xpaths:
            text = abs_xpath.xpath('./text()')
            text = text[-1].replace('\n', '').strip()

            TEXT = abs_xpath.xpath('./*/text()')
            TEXT = TEXT[-1].replace('\n', '').strip() if TEXT else ''

            Abs += TEXT + text + '\n'
        for a in find_abstract:
            if a in Abs:
                L.append([title, Abs, url_article])
                break

pd.DataFrame(L).to_excel('1.xlsx', encoding='gb18030', header=False, index=False)
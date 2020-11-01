import requests
import re

i=1
def make_context(serch_url):

    #print(serch_url)
    get_url_info = requests.get(serch_url)
    #print(get_url_info.text)
    context = get_url_info.text
    return context

def crawler(serch_url):
    global i
    get_url_info = requests.get(serch_url)
    context = get_url_info.text
    split_lists = context.split('<li>')
    for li in split_lists[1:]:
        print(i)
        #print(li)
        #正規表現で<から始まって0以上の複数文字のあと>で終わるものをremoveしたい
        #最短マッチ、最も短いマッチ、最長マッチ
        #<a aria-label="Page 2"とかで次のページに進む
        print(re.sub('<.*?>','',li))
        i+=1

keyword = input()
serch_url = "https://search.yahoo.co.jp/search?p=" + keyword

context = make_context(serch_url)
#print(context)
crawler(serch_url)
split_nextpage = context.split('&nbsp;&nbsp')
for page in range(5):
    #next_url = re.search('\".*\"?',split_nextpage[page+2])
    #[^...]・・・[]に含まれている文字以外にマッチ
    next_url = re.search('\"[^\"]*\"',split_nextpage[page+2])
    serch_url = next_url.group().replace('\"','')
    crawler(serch_url)



# for nextpage in split_nextpage:
#     print(i)
#     print(nextpage)
#     i+=1

# for page in range(5):
#     next_url = re.search('\".*\"?',split_nextpage[page+2])
#     next_url = re.search('\"[^\"]*\"',split_nextpage[page+2])
#     serch_url = next_url.group().replace('\"','')
import requests
get_url_info = requests.get('https://www.yahoo.co.jp/')
# print(get_url_info.text)
context = get_url_info.text
main_news = context.split('主要 ニュース')
# print(main_news)
i=0

#main_news[2]の中に主要ニュースの大枠の部分が入っている

# for news in main_news:
#     print(i)
#     print(news)
#     i+=1


# shusou=main_news[2].split('首相')
# print(shusou[1])


split_h1 = main_news[2].split('h1 class=')
#print(main_news[2])
#yahooのトップニュースはいつも9個であると仮定
for sph1 in split_h1[1:9]:
    ans=sph1.split('\">')
    cut_span = ans[2].split('</span>')
    # print(ans[2])
    print(cut_span[0])
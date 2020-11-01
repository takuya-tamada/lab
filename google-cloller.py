import requests
import sys
import codecs
import re

keyword = input()
#print(keyword)
serch_url = "https://www.google.com/search?q=" + keyword
#serch_url = "https://www.google.com/search?q=%E5%A4%A7%E9%98%AA%E5%BA%9C%E7%AB%8B%E5%A4%A7&rlz=1C5CHFA_enJP789JP789&sxsrf=ALeKk02tCMz07Hhj98HqEGodo1auFj61jg:1603034628532&ei=BF6MX6OEIJfZhwO-wJaQCg&start=10&sa=N&ved=2ahUKEwijluKsub7sAhWX7GEKHT6gBaIQ8tMDegQIKxAz&biw=1440&bih=721
#serch_url = "https://www.google.com/search?sxsrf=ALeKk00TRIdFBhH65ZSIvDb0PeCgUPLTNw%3A1601946340052&ei=5MJ7X47jApOGoATVsbboCg&q=%E3%81%8A%E3%81%8A%E3%81%8A&oq=%E3%81%82%E3%81%82%E3%81%82&gs_lcp=CgZwc3ktYWIQAzIECAAQQzIKCAAQsQMQsQMQQzICCAAyBAgAEEMyBggAEAoQQzICCAAyAggAMggIABCxAxCxAzoECAAQRzoKCAAQsQMQgwEQBDoECAAQBDoHCAAQsQMQBDoICAAQChBDECo6BwgAELEDEEM6CwgAELEDEAoQQxAqOg8IABCxAxCDARAEEEYQgAI6DggAELEDEIMBELEDEIMBUMIZWLo5YO47aAJwAngAgAFriAGjC5IBBDE0LjKYAQCgAQGqAQdnd3Mtd2l6sAEAyAEIwAEB&sclient=psy-ab&ved=0ahUKEwiO5bCU457sAhUTA4gKHdWYDa0Q4dUDCA0&uact=5"
#serch_url = "https://www.google.com/search?q=%E3%81%82%E3%81%82&rlz=1C5CHFA_enJP789JP789&oq=%E3%81%82%E3%81%82&aqs=chrome..69i57j0l6j69i60.759j0j7&sourceid=chrome&ie=UTF-8"

get_url_info = requests.get(serch_url)
# encode_text = get_url_info.text.decode('cp932')
#endocde_text = '&#12362;&#12362'.decode('utf-8')
# print(get_url_info.text)
# print(get_url_info.encoding)
# get_url_info.decode(get_url_info.encoding)

#text = get_url_info.decode('utf-8')
#get_url_info.encoding = get_url_info.apparent_encoding

#ISO、、をUTF8に変換する、NKF文字コード変換つーる
#&#のあとはUNIコードに基づいた10進数、javascriptによって日本語に変換している、UNIコードの10進表記から文字に変えればいい


get_url_info.encoding = 'UTF-8'
text = get_url_info.text
text_urf8 = text.encode('UTF-8')
# print(chr(12345)

charcodes = re.findall('&#.*?;',text)
# print(charcodes)＃

# remove_symbol = [re.sub('&#?','',charcodes)]

text_code = re.sub(r'(&#.*?;)',r'\1',text)

# print(text_code)

remove_symbol = []
for char in charcodes:
    # re.sub('&#','',char)
    # re.sub(';','',char)
    char = char.strip('&#')
    char = char.strip(';')
    # remove_symbol.append(char)
    remove_symbol.append(chr(int(char)))


for i in range(len(charcodes)):
    text = text.replace(charcodes[i],remove_symbol[i])

#&#で始まって;で終わるものを抽出して配列に入れる。それをchrした配列を作り直して、前者と後者を置換した。ここまでやらなあかんもんなのか？
print(text)

split_lists = text.split('<div class="BNeawe vvjwJb AP7Wnd">')
#split_lists = text.split('<div class="BNeawe s3v9rd AP7Wnd">')
for i,content in enumerate(split_lists[1:len(split_lists)]):
    print(i)
    gaiyou = content.split('<div class="BNeawe s3v9rd AP7Wnd">')
    gaiyou_spl = content.split('<div class="BNeawe UPmit AP7Wnd">')
    # print(content)
    # print(gaiyou[2])
    # gaiyou = gaiyou_spl[2].split('<')
    # print(gaiyou[2])

#日本語が何文字以上続くのかで切ろうとした→空白やコンマがマッチしない
# overviews = re.findall('[亜-熙ぁ-んァ-ヶ]{10,}',text)
# print(overviews)



# print(remove_symbol)
# print(text_urf8.decode('UTF-8'))
#print(text.decode('unicode-escape')) 
# print(get_url_info.text)
# sys.stdin  = codecs.getreader('utf_8')(sys.stdin)
# for line in sys.stdin:
#     print(line)
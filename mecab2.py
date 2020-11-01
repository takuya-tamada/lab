import MeCab 
import sys
import sqlite3
import requests
import re
def main():
    # extraction_noun()
    # output_input_text()
    # make_db()
    # make_article_db()
    # serch_newspaper()
    # add_db()
    # open_db()
    open_id_db()
    # tf()

def read_text():
    text = '今日はいい天気ですね'
    mecab = MeCab.Tagger('/Users/tamadatakuya/Downloads/mecab-ipadic-neologd').parse(text)
    return(mecab)

def input_text():
    infile = 'tenki.txt'
    with open(infile ,encoding="utf-8") as f:
        text = f.read()
    mecab = MeCab.Tagger('/Users/tamadatakuya/Downloads/mecab-ipadic-neologd').parse(text)
    return(mecab)

def output_read_text():
    print(read_text())

def output_input_text():
    print(input_text())

#形態素分析の結果を配列に入れる動作だけ切り出してもいいのではないか、、、
def extraction_noun():
    text = read_text().replace('\nEOS','')
    # print(text)
    #平テキストを改行文字でスプリット
    classify_word = text.split('\n')
    # print(classify_word)
    classify_kind = []
    nouns = []
    nouns_set = set()
    for i in range(len(classify_word)-1):
        get_kind = classify_word[i].split('\t')
        print(get_kind[0])
        classify_kind.append(get_kind[1].split(','))
        nouns.append(classify_kind[i][0])
        nouns_set.add(classify_kind[i][0])
    #重複を許していいのならnouns,許さないならnouns_setを出力
    # print(nouns_set)
    print(nouns)
    # print(classify_word[0])

def make_db():
    dbname = 'ARTICLE.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(
        'create table articles(id integer primary key autoincrement, article_id integer,part_of_speech text,part_of_speech_subclass1 text,part_of_speech_subclass2 text,part_of_speech_subclass3 text,inflected_form text,utilization_type text,prototype text,reading text,pronoun text)'
         
    )
    cur.execute(
        'create table article_ids(article_id integer primary key autoincrement, title text, tf real,df real,tfidf real)'
    )
    conn.commit()
    conn.close()

def make_article_db():
    dbname = 'ARTICLE_ID.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(
        'create table article_ids(article_id integer primary key autoincrement, title text, tf real,df real,tfidf real)'
    )
    conn.commit()
    conn.close()

def add_db():
    dbname = 'ARTICLE.db'
    conn = sqlite3.connect(dbname)

    cur = conn.cursor()

    #mecab_analyzeには単語の数の配列の中に,で区切られたテキストが１つ入っている設定
    title,mecab_analyzes = serch_newspaper() 
    sql_id = 'insert into article_ids(title) values(?)'
    title_list = (title,)
    cur.execute(sql_id,title_list)
    conn.commit()
    cur.execute('select article_id from article_ids where rowid = last_insert_rowid();')
    article_id = cur.fetchall()[0][0]
    # print(article_id)
    conn_id.close()
    for content in mecab_analyzes:
        _str = content.split(',')
        # print(content)
        #品詞、品詞再分類1、品詞細分類2、品詞細分類3、活用形、活用型、原型、読み、発音
        part_of_speech = _str[0]
        part_of_speech_subclass1 = _str[1]
        part_of_speech_subclass2 = _str[2]
        part_of_speech_subclass3 = _str[3]
        inflected_form = _str[4]
        utilization_type = _str[5]
        prototype = _str[6]
        if len(_str)<10:
            reading = _str[0]
            pronoun = _str[0]
        else:
            reading = _str[7]
            pronoun = _str[8]
        # print(part_of_speech)
        sql = 'insert into articles (article_id,part_of_speech,part_of_speech_subclass1,part_of_speech_subclass2,part_of_speech_subclass3,inflected_form,utilization_type,prototype,reading,pronoun) values (?,?,?,?,?,?,?,?,?,?)'
        namelist = (article_id,part_of_speech,part_of_speech_subclass1,part_of_speech_subclass2,part_of_speech_subclass3,inflected_form,utilization_type,prototype,reading,pronoun)
        cur.execute(sql, namelist)
    conn.commit()
    conn.close()

def open_db():
    dbname = 'ARTICLE.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('select * from articles')
    #where name = "シーテック\u3000ダッシュボード透明化、GSPなくても自動走行…電子部品メーカー、自動車支える技術アピール"
    print(cur.fetchall())
    conn.commit()
    conn.close()

def open_id_db():
    dbname = 'ARTICLE.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('select * from article_ids')
    #where name = "シーテック\u3000ダッシュボード透明化、GSPなくても自動走行…電子部品メーカー、自動車支える技術アピール"
    print(cur.fetchall())
    conn.commit()
    conn.close()

def serch_newspaper():
    serch_url = 'https://www.sankei.com/politics/news/201026/plt2010260004-n1.html'
    get_url_info = requests.get(serch_url)
    title,content =  sankei_format(get_url_info.text)
    mecab_analyzes = make_news_word_list(content)
    return title,mecab_analyzes

def make_news_word_list(content):
    news_word_list = []
    mecab = MeCab.Tagger('/Users/tamadatakuya/Downloads/mecab-ipadic-neologd').parse(content)
    mecab_splitn = mecab.split('\n')

    # print(mecab_splitn)
    # mecab = [row.replace('\t','ああああ') for row in mecab]

    for i in range(len(mecab_splitn)):
        mecab_splitn[i] = mecab_splitn[i].replace('\t',',')
        # print(mecab_splitn[i])
    del mecab_splitn[len(mecab_splitn)-1]
    del mecab_splitn[len(mecab_splitn)-1]
    del mecab_splitn[0]
    # print(mecab_splitn[len(mecab_splitn)-1])
    return mecab_splitn



def sankei_format(text):
    title_obj = re.search('pis_title\">.*?</span>',text)
    title = title_obj.group().replace('pis_title\">','').replace('</span>','')
    title = title.replace('　','')
    # print(text)
    # print(title)
    content_list = re.findall('<p>.*</p>',text)
    content_list = [content.replace('<p>','').replace('</p>','') for content in content_list]
    content = ''.join(content_list)
    # print(content)
    return title,content

def tf():
    target_article = SI()
    print(target_article)
    dbname = 'ARTICLE.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    # cur.execute('select count(*) from articles where name = "日本初のラーメンブーム生んだ「来々軒」復活\u3000ラー博で今月から" ')
    sql = 'select count(*) from articles where name = (?)'
    namelist = (target_article)
    cur.execute(sql, (target_article,))
    total_words = int(cur.fetchall()[0][0])
    # print(total_words)
    sql = 'SELECT part_of_speech, COUNT( part_of_speech ) FROM articles where name = (?) GROUP BY part_of_speech'
    cur.execute(sql,(target_article,))
    # print(cur.fetchall())
    count_n = cur.fetchall()
    print(target_article + 'における各単語のIF')
    for word in count_n:
        print(word[0],int(word[1])/total_words)
    
    conn.commit()
    conn.close()


def SI(): return sys.stdin.readline().strip()

if __name__ == '__main__':
    main()


# # テキスト直打ち↓
# text = "今日はいい天気ですね"

# infile = 'tenki.txt' 
# with open(infile ,encoding="utf-8") as f:
#     text = f.read()

# #mecab-ipadic-NEologdという辞書で形態素解析を行う
# mecab = MeCab.Tagger('/Users/tamadatakuya/Downloads/mecab-ipadic-neologd').parse(text)
# #mecab = MeCab.Tagger().parse(text)
# print(mecab)


import MeCab 

# # テキスト直打ち↓
# text = "今日はいい天気ですね"

infile = 'tenki.txt' 
with open(infile ,encoding="utf-8") as f:
    text = f.read()

#mecab-ipadic-NEologdという辞書で形態素解析を行う
mecab = MeCab.Tagger('/Users/tamadatakuya/Downloads/mecab-ipadic-neologd').parse(text)
#mecab = MeCab.Tagger().parse(text)
print(mecab)


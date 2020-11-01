#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
# import config
from requests_oauthlib import OAuth1Session

# OAuth認証部分
CK      = 'APB1qO6MVdqUXlgiVIv1MDnaM'
CS      = '6QocQvs0HL8S75XVF4DvwiRt2ednHfrFwjR2dTU0XQQv1ihxiL'
AT      = '1143336983109885952-k7OB0ATrVNO5HLJIokNGLk0aUVCP1E'
ATS     = 'Y12kQJwxvX325CUW3tyuCO3L11Ziyp5aPVTPMKeAO48pT'
twitter = OAuth1Session(CK, CS, AT, ATS)

# Twitter Endpoint(検索結果を取得する)
url = 'https://api.twitter.com/1.1/search/tweets.json'

# Enedpointへ渡すパラメーター
keyword = '福留'

params ={
         'count' : 100,      # 取得するtweet数
         'q'     : keyword  # 検索キーワード
         }

req = twitter.get(url, params = params)

if req.status_code == 200:
    res = json.loads(req.text)
    for line in res['statuses']:
        print(line['text'])
        print('*******************************************')
else:
    print("Failed: %d" % req.status_code)
import argparse
import json
import os
import requests
import sys


parser = argparse.ArgumentParser()
# JSON形式で出力
parser.add_argument("-j", "--json", help="Print as JSON format", action='store_true', default='false')
# 記事IDを表示
parser.add_argument("-i", "--id", help="Print ID", action='store_true', default='false')


parser_article_state = parser.add_mutually_exclusive_group()
parser_article_state.add_argument("-a", "--all", help="Get all articles", action='store_true', default='false')
parser_article_state.add_argument("-r", "--archive", help="Get archived articles only", action='store_true', default='false')
parser_article_state.add_argument("-u", "--unread", help="Get unread articles only (default)", action='store_true', default='true')

args = parser.parse_args()

try:
    os.environ['CONSUMER_KEY'] == None
except KeyError:
    sys.stderr.write('Set your consumer_key to CONSUMER_KEY')
    os._exit(2)

try:
    os.environ['ACCESS_TOKEN'] == None
except KeyError:
    sys.stderr.write('Set your access_key to ACCESS_KEY')
    os._exit(3)

# どの状態の一覧を読み込むか？
if args.archive == True:
    state = "archive"
elif args.all == True:
    state = "all"
else:
    state = "unread"


payload ={ 
    'consumer_key' : os.environ['CONSUMER_KEY'],
    'access_token' : os.environ['ACCESS_TOKEN'],
    'state' : state
    }


url = 'https://getpocket.com/v3/get'

try:
    res = requests.post(url, data=payload)
    res.status_code == requests.codes.ok
except:
    sys.stderr.write('Some error occured.')
    sys.exit(1)

items = res.json()

# 表示部
if args.json == True:
    print (items)
else:
    for item_id in items['list']:
        url = items['list'][item_id]['given_url']
        id = items['list'][item_id]['item_id']
        # --idがあるなら、記事ID込で表示
        if args.id == True:
            print(id + "\t" + url)
        else:
            print(url)
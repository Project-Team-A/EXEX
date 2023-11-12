
import datetime
import requests
import json
#import slackweb

# 地震確認：基準時間設定
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
hour_ago = now - datetime.timedelta(hours=1)
base_time = hour_ago.strftime('%Y/%m/%d %H:%M:%S') # 2021/11/04 17:37:28

# payload:検索条件
limit = 1
min_scale = 55 # 最大震度の下限。10(震度1)、20(震度2)、30(震度3)、40(震度4)、45(震度5弱)、50(震度5強)、55(震度6弱)、60(震度6強)、70(震度7)。

if min_scale < 45:
    min_intensity = '震度１～４'
elif min_scale < 55:
    min_intensity = '震度５'
elif min_scale < 70:
     min_intensity = '震度６' 
elif min_scale >= 70:
    min_intensity = '震度７'

# 地震情報：概要抽出
#url = "https://api.p2pquake.net/v2/jma/quake"
url = "https://api-v2-sandbox.p2pquake.net/v2/history?codes=556&limit=10"
limit=5    #ここで最新のn件を取得

params = {
    "codes": "551",
    "limit": 10
}

payload = {"limit":limit, "min_scale":min_scale}

r = requests.get(url, params=params)
if r.status_code != 200:
    print("Failed to get the data from API.")
    exit()

data_list = r.json()#変更

found = False
for data in data_list:
    info_url = url + '/' + data['id']
    info_r = requests.get(info_url)
    if info_r.status_code == 400:
        print("API Response Error:", info_r.text)
        continue

    try:
        info_data = json.loads(info_r.text)
    except json.JSONDecodeError:
        print("Failed to decode JSON from the response.")
        continue

    for point in info_data['points']:
        if "茅ヶ崎市" in point['addr']:
            quake_date = info_data['earthquake']['time']
            print(f"震度 in 茅ヶ崎市: {point['scale'] / 10} (震度{point['scale']}), Date and Time: {quake_date}")  # 震度情報をプリントアウト
            found = True
            break

    if found:
        break

# 地震情報：詳細抽出
info_url = url + '/' + data_list[0]['id']
info_r = requests.get(info_url)
#追加
print("API Response:", info_r.text)
print(info_r.status_code)
try:
    info_data = json.loads(info_r.text)
except json.JSONDecodeError:
    print("Failed to decode JSON from the response.")
     # ここで適切なエラーハンドリングを行います。例えば、エラーメッセージを表示して処理を終了するなど。
    exit()  # スクリプトの実行を終了します
#追加
info_data = json.loads(info_r.text)


#追加
print(info_data['points'][0])
#追加

quake_time = info_data['earthquake']['time']
name = info_data['earthquake']['hypocenter']['name']
maxscale = info_data['earthquake']['maxScale']

# 震度判定
if maxscale < 45:
    intensity = '震度４以下'
elif maxscale < 55:
    intensity = '震度５'
elif maxscale < 70: intensity = '震度６' 
elif maxscale >= 70:
    intensity = '震度７以上'

# （min_scale）以上に該当する都道府県を出力　
#追加
target_city = "茅ヶ崎市" #茅ヶ崎市に定義
found=False #茅ヶ崎市が見つからなかった時のフラグ#追加


#取得したすべての地震情報の中で「茅ヶ崎市」が含まれているかどうかを明示的にチェックするコード
for data in data_list:
    info_url = url + '/' + data['id']
    info_r = requests.get(info_url)
    info_data = json.loads(info_r.text)
    for point in info_data['points']:
        if "茅ヶ崎市" in point['addr']:
            quake_date = info_data['earthquake']['time']
        print(f"震度 in 茅ヶ崎市: {point['scale'] / 10} (震度{point['scale']}), Date and Time: {quake_time}") #震度情報をプリントアウト
        break
    
#

if not found:
    print(f"No recent earthquake data found for {target_city}.")
#追加

region = []
for i in info_data['points']:
    if i['scale'] >= min_scale and target_city in i['addr']:
        region.append(i['name'])


# 重複する都道府県を１つに処理
region = list(dict.fromkeys(region))
str_region = "\n".join(region)


































""" slack設定
slack = slackweb.Slack(url = "https://hooks.slack.com/services/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")
blocks = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "<!channel> %s以上の地震を観測しました。状況についてお知らせください。" % (min_intensity)
        }
    },
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "【最大%s】の地震を観測" % (intensity)
        }
    },
{
        "type": "divider"
    },
    {
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": "*発生時間*\n%s" % (quake_time)
            },
            {
                "type": "mrkdwn",
                "text": "*震源地域*\n%s（%s）" % (name, intensity)
            },
        ]
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*%s以上の都道府県*\n%s" % (min_intensity, str_region)
        }
    },
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "従業員の皆様へお願い"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":one: 揺れがおさまるまで身の安全を確保し、落ち着いて行動しましょう！\n\n:two: ケガ等が無いか *「24時間以内 :clock3:」*  にスタンプや返信で反応をお願いします:bow:"
        }
    },
{
    "type": "divider"
    },
    {
        "type": "divider"
    }
]

# Slack通知：基準時間より最新の地震計測であれば通知
print("前回のチェック時間")
print(base_time)
print("直近発生した地震の時間")
print(quake_time)
if base_time < quake_time:
    print('実行時間の1時間前よりも大きい時間＝更新されている＝通知')
    slack.notify(text="地震発生！ケガ等が無いかお知らせください！", blocks=blocks)
elif base_time > quake_time:
    print('実行時間の1時間前よりも小さい時間＝更新されていない＝処理終了')
    """
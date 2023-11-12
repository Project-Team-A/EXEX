#インターネット上からデータを取得するためのモジュールをインポート
import requests
#リクエストするURLを指定(最新の地震情報のデータを取得することができるURL)
p2pquake_url = 'https://api.p2pquake.net/v2/history?codes=551&limit=1'
#リクエスト(データを取得する)
p2pquake_json = requests.get(p2pquake_url).json()

#震央地名を取り出して、変数Eq_nameに代入する
Eq_name = p2pquake_json[0]["earthquake"]["hypocenter"]["name"]
print(Eq_name)

from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # テストデータの定義
    test_data = [
      {
        "earthquake": {
          "time": "2023-11-06T12:00:00Z",
          "hypocenter": {
            "name": "茅ヶ崎市",
            "magnitude": 5.0,
            "depth": 10,
            "latitude": 35.3302,
            "longitude": 139.4053
          }
        }
      }
    ]

    # HTMLテンプレートにテストデータを渡して表示
    return render_template('index.html', earthquake=test_data[0])

if __name__ == '__main__':
    app.run(debug=True)
    
"""""
# 地震データのAPIエンドポイント
P2PQUAKE_URL = 'https://api.p2pquake.net/v2/history?codes=551&limit=10'

@app.route('/')
def index():
    # 地震データを取得
    response = requests.get(P2PQUAKE_URL)
    earthquakes = response.json()
    
    # 茅ヶ崎市の地震情報をフィルタリング
    chigasaki_earthquakes = [eq for eq in earthquakes if '茅ヶ崎市' in eq.get('earthquake', {}).get('hypocenter', {}).get('name', '')]
    
    # 最新の地震情報を取得
    latest_earthquake = chigasaki_earthquakes[0] if chigasaki_earthquakes else None
    
    # HTMLテンプレートにデータを渡して表示
    return render_template('index.html', earthquake=latest_earthquake)

if __name__ == '__main__':
    app.run(debug=True)
"""""
from flask import Flask, render_template
import requests 

app = Flask(__name__)

@app.route('/')
def index():
    # リアルタイム地震データの取得
    p2pquake_url = 'https://api.p2pquake.net/v2/history?codes=551&limit=1'
    response = requests.get(p2pquake_url)
    real_time_data = response.json()[0] if response.status_code == 200 else None

    # テストデータの定義
    test_data = [
      {
        "earthquake": {
          "time": "2023-11-06T12:00:00Z",
          "hypocenter": {
            "name": "神奈川県茅ヶ崎市",
            "magnitude": 3.4,
            "maxScale": 3,
            "depth": 10,
            "latitude": 35.3302,
            "longitude": 139.4053
          }
        }
      }
    ]

    # テンプレートにリアルタイムデータとテストデータを渡す
    return render_template('ex.html', real_time_data=real_time_data, test_data=test_data)

if __name__ == '__main__':
    app.run(debug=True)

    
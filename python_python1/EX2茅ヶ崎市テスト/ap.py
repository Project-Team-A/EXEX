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

    # HTMLテンプレートにテストデータを渡して表示aa
    return render_template('ex.html', earthquake=test_data[0])

if __name__ == '__main__':
    app.run(debug=True)
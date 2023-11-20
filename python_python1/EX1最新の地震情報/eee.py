from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # 地震情報のAPIエンドポイント
    p2pquake_url = 'https://api.p2pquake.net/v2/history?codes=551&limit=1'
    
    # APIから地震情報を取得
    try:
        response = requests.get(p2pquake_url)
        response.raise_for_status()  # ステータスコードが200以外の場合はエラーを発生させる
        earthquake_info = response.json()[0]  # 最新の地震情報を取得
    except requests.RequestException as e:
        earthquake_info = None
        print(f"Error fetching earthquake data: {e}")

    # 地震情報が取得できたかチェック
    if earthquake_info:
        # 震央地名
        eq_name = earthquake_info["earthquake"]["hypocenter"]["name"]
        # 震度
        max_intensity = earthquake_info["earthquake"]["maxScale"]
        # 日時
        eq_datetime = earthquake_info["earthquake"]["time"]
    else:
        eq_name = max_intensity = eq_datetime = "データが取得できませんでした"

    # 地震情報をHTMLテンプレートに渡してレンダリング
    return render_template('index.html', eq_name=eq_name, max_intensity=max_intensity, eq_datetime=eq_datetime)

if __name__ == '__main__':
    app.run(debug=True)
